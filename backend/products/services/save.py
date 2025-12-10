import logging
from datetime import datetime

import requests
from django.conf import settings
from django.db import transaction

from products.models import Bank, Product, ProductOption

logger = logging.getLogger(__name__)

API_KEY = settings.FSS_API_KEY
BASE_URL = settings.FSS_BASE_URL

GROUP_CODES = ["020000", "030200", "030300", "050000", "060000"]  # 은행, 여신전문, 저축은행, 보험, 금융투자 

def _call_fss_api(service_name: str, top_fin_grp_no: str, page_no: int) -> dict:
    """
    service_name:
      - 'depositProductsSearch' (정기예금)
      - 'savingProductsSearch'  (적금)
    """
    url = f"{BASE_URL}{service_name}.json"
    params = {
        "auth": API_KEY,
        "topFinGrpNo": top_fin_grp_no,
        "pageNo": page_no,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data


def _is_active_product(dcls_strt_day: str | None, dcls_end_day: str | None) -> bool:
    '''
    금융상품 정보는 매월 20일 정기적으로 제공받아 공시된 정보임
    시작일이 오늘보다 크면 미래니까 추천되는 것을 막음
    공시 종료일이 오늘보다 작으면 지난 상품이니까 추천되는 것을 막음
    '''
    today = datetime.today().strftime("%Y%m%d")
    # 시작일 체크
    if dcls_strt_day:
        try:
            if dcls_strt_day > today:
                return False
        except Exception:
            pass  # 시작일이 이상하면 일단 무시

    # 종료일 체크
    if dcls_end_day:
        try:
            if dcls_end_day < today:
                return False
        except Exception:
            pass

    return True


@transaction.atomic
def _save_page_to_db(product_type: str, base_list: list[dict], option_list: list[dict]) -> None:
    """
    한 페이지 분(baseList + optionList)을 DB에 저장.
    - Bank: fin_co_no 기준으로 get_or_create → 중복 방지
    - Product: (bank, product_type, fin_prdt_cd) 기준으로 update_or_create → 중복 없이 갱신
    - ProductOption: 해당 product 의 기존 옵션 싹 지우고 새로 생성 → 중복 없음
    """

    # (fin_co_no, fin_prdt_cd) 기준으로 옵션을 묶어둔다
    option_map: dict[tuple[str | None, str | None], list[dict]] = {}
    for opt in option_list:
        key = (opt.get("fin_co_no"), opt.get("fin_prdt_cd"))
        option_map.setdefault(key, []).append(opt)

    for item in base_list:
        fin_co_no = item.get("fin_co_no")
        kor_co_nm = item.get("kor_co_nm") or ""

        # 1) Bank: 코드 기준으로 중복 방지
        bank, _ = Bank.objects.get_or_create(
            fin_co_no=fin_co_no,
            defaults={"kor_co_nm": kor_co_nm},
        )
        # 이름이 바뀐 경우 갱신
        if bank.kor_co_nm != kor_co_nm:
            bank.kor_co_nm = kor_co_nm
            bank.save()

        # 2) Product: (bank, product_type, fin_prdt_cd) 기준으로 중복 없이 upsert
        fin_prdt_cd = item.get("fin_prdt_cd")
        dcls_strt_day = item.get("dcls_strt_day") or ""
        dcls_end_day = item.get("dcls_end_day") or ""
        is_active = _is_active_product(dcls_strt_day, dcls_end_day)

        max_limit = item.get("max_limit")
        if max_limit is None:
            max_limit = 0

        product, _ = Product.objects.update_or_create(
            bank=bank,
            product_type=product_type,
            fin_prdt_cd=fin_prdt_cd,
            defaults={
                "fin_prdt_nm": item.get("fin_prdt_nm", ""),
                "dcls_month": item.get("dcls_month", ""),
                "join_way": item.get("join_way") or "",
                "join_member": item.get("join_member") or "",
                "join_deny": item.get("join_deny") or "",
                "spcl_cnd": item.get("spcl_cnd") or "",
                "etc_note": item.get("etc_note") or "",
                "mtrt_int": item.get("mtrt_int") or "",
                "max_limit": max_limit,
                "dcls_strt_day": dcls_strt_day,
                "dcls_end_day": dcls_end_day,
                "fin_co_subm_day": item.get("fin_co_subm_day") or "",
                "is_active": is_active,
            },
        )

        # 3) 옵션: 해당 상품의 옵션을 싹 지우고, 새로 insert → 중복 없음
        ProductOption.objects.filter(product=product).delete()

        for opt in option_map.get((fin_co_no, fin_prdt_cd), []):
            # 기본값은 공백 → 정기예금(DEPOSIT)일 때는 그냥 빈 값으로 남김
            rsrv_type = ""
            rsrv_type_nm = ""

            # 적금(SAVING)일 때만 적립유형 세팅
            if product.product_type == Product.ProductType.SAVING:
                rsrv_type = opt.get("rsrv_type") or ""
                rsrv_type_nm = opt.get("rsrv_type_nm") or ""

            ProductOption.objects.create(
                product=product,
                intr_rate_type=opt.get("intr_rate_type") or "",
                intr_rate_type_nm=opt.get("intr_rate_type_nm") or "",
                rsrv_type=rsrv_type,
                rsrv_type_nm=rsrv_type_nm,
                save_trm=opt.get("save_trm") or "",
                intr_rate=opt.get("intr_rate"),
                intr_rate2=opt.get("intr_rate2"),
            )

def sync_deposit_products():
    '''
    정기예금 전체 동기화 
    '''
    for grp in GROUP_CODES:
        page_no = 1
        while True:
            data = _call_fss_api("depositProductsSearch", grp, page_no)
            result = data.get("result") or {}

            err_cd = result.get("err_cd")
            if err_cd and err_cd != "000":
                logger.error(f"[DEPOSIT] grp={grp}, page={page_no}, err_cd={err_cd}, msg={result.get('err_msg')}")
                break

            base_list = result.get("baseList") or []
            option_list = result.get("optionList") or []

            if not base_list:
                # 더 이상 데이터가 없으면 종료
                break

            _save_page_to_db(Product.ProductType.DEPOSIT, base_list, option_list)

            now_page = int(result.get("now_page_no", page_no))
            max_page = int(result.get("max_page_no", now_page))

            if now_page >= max_page:
                break
            page_no += 1


def sync_saving_products():
    """
    적금 전체 동기화 (권역별 + 페이지 전체)
    """
    for grp in GROUP_CODES:
        page_no = 1
        while True:
            data = _call_fss_api("savingProductsSearch", grp, page_no)
            result = data.get("result") or {}

            err_cd = result.get("err_cd")
            if err_cd and err_cd != "000":
                logger.error(f"[SAVING] grp={grp}, page={page_no}, err_cd={err_cd}, msg={result.get('err_msg')}")
                break

            base_list = result.get("baseList") or []
            option_list = result.get("optionList") or []

            if not base_list:
                break

            _save_page_to_db(Product.ProductType.SAVING, base_list, option_list)

            now_page = int(result.get("now_page_no", page_no))
            max_page = int(result.get("max_page_no", now_page))

            if now_page >= max_page:
                break
            page_no += 1


def sync_all_products():
    """
    예금 + 적금 전체 동기화
    """
    logger.info("=== 정기예금 상품 동기화 시작 ===")
    sync_deposit_products()
    logger.info("=== 정기예금 상품 동기화 완료 ===")

    logger.info("=== 적금 상품 동기화 시작 ===")
    sync_saving_products()
    logger.info("=== 적금 상품 동기화 완료 ===")