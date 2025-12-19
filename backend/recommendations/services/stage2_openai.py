from __future__ import annotations

import os
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from django.conf import settings
from django.utils import timezone

from products.models import Product, ProductOption


BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")

GMS_URL = getattr(
    settings,
    "GMS_URL",
    "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions",
)
DEFAULT_MODEL = getattr(settings, "GMS_MODEL", "gpt-5-mini")
DEFAULT_TIMEOUT = int(getattr(settings, "GMS_TIMEOUT", 30))


@dataclass
class Stage2Output:
    product_id: int # 최종 선택된 상품 id
    option_id: int # 최종 선택된 옵션 id
    reasons: List[str] # 선택 근거
    warnings: List[str] # 주의사항
    used_fallback: bool # GMS 실패 시 규칙 기반 풀백 여부 


DEVELOPER_MSG = "Answer in Korean. 반드시 JSON만 출력하고 다른 텍스트는 출력하지 마세요."

SYSTEM_INSTRUCTIONS = """\
당신은 예/적금 상품의 옵션(ProductOption)을 최종 선택하는 엔진입니다.

입력:
- user: 사용자 프로필(요약)
- goal: 목표(목표금액/기간/목적)
- top10_product_ids: Stage1 Top10 상품 id
- candidates: 후보 옵션 리스트(여기 안에서만 option_id를 선택)
- product_texts: 상품 단위 텍스트 정보(spcl_cnd/etc_note/mtrt_int 등)

제약:
- 반드시 candidates 안에서 option_id를 1개 선택합니다.
- 반드시 top10_product_ids 안에서 product_id를 선택합니다.
- 출력은 오직 JSON 객체 1개만 출력합니다(코드블록/설명/추가 텍스트 금지).

우선순위:
1) 목표 term_months와 save_trm(개월)이 같거나 가장 가까운 옵션
2) purpose가 YIELD면 intr_rate2(우대금리) 우선(기간이 너무 어긋나면 감점)
   그 외 목적은 기간 적합 최우선 + 금리 tie-break
3) product_texts의 spcl_cnd / etc_note / mtrt_int에서 확인되는 리스크/제약사항이 있으면 warnings에 요약

반드시 아래 스키마로 출력:
{
  "product_id": <int>,
  "option_id": <int>,
  "reasons": [<string>, <string>, ...],   # 2~5개
  "warnings": [<string>, ...]            # 0~4개
}
"""

# User모델 정보 -> dict화 (사용자 맥락 전달)
def _user_ctx(user) -> Dict[str, Any]:
    today = timezone.now().date()
    age = (today - user.birth).days // 365 if getattr(user, "birth", None) else None
    return {
        "age": age,
        "gender": getattr(user, "gender", None),
        "credit_score": getattr(user, "credit_score", None),
        "assets": getattr(user, "assets", None),
        "salary": getattr(user, "salary", None),
        "average_monthly_spend": getattr(user, "average_monthly_spend", None),
        "tender": getattr(user, "tender", None),
    }

# Moathon모델에 들어갈 추천 요청에 포함된 목표 정보 -> dict화 (목표 맥락 전달)
def _goal_ctx(goal: Dict[str, Any]) -> Dict[str, Any]:
    target_amount = int(goal["target_amount"])
    start_amount = int(goal["start_amount"])
    term_months = int(goal["term_months"])
    need_amount = max(target_amount - start_amount, 0)
    need_per_month = need_amount / (term_months or 1)
    return {
        "purpose": goal["purpose"],
        "target_amount": target_amount,
        "start_amount": start_amount,
        "term_months": term_months,
        "need_amount": need_amount,
        "need_per_month": need_per_month,
    }

# 특정 상품안에 있는 옵션이 많을 경우 상품당 n(3)로 한정
# 선택 기준은 ranked
def shortlist_options_for_product(
    product_id: int,
    term_months: int,
    per_product: int = 3,
) -> List[Dict[str, Any]]:
    qs = (
        ProductOption.objects
        .select_related("product")
        .filter(product_id=product_id)
        .values(
            "id", "product_id",
            "save_trm", "intr_rate", "intr_rate2",
            "intr_rate_type_nm", "rsrv_type_nm",
            "product__join_deny",
        )
    )
    opts = list(qs)
    if not opts:
        return []

    # 우대 금리가 존재하면 우대금리 우선, 아니면 기존 금리 
    def rate2(o: Dict[str, Any]) -> float:
        v = o.get("intr_rate2")
        if v is None:
            v = o.get("intr_rate")
        try:
            return float(v) if v is not None else 0.0
        except Exception:
            return 0.0

    ranked = sorted(
        opts,
        key=lambda o: (abs(int(o.get("save_trm")) - int(term_months)), -rate2(o)),
    )[:per_product]

    return [
        {
            "option_id": int(o["id"]),
            "product_id": int(o["product_id"]),
            "save_trm": o.get("save_trm"),
            "intr_rate": o.get("intr_rate"),
            "intr_rate2": o.get("intr_rate2"),
            "intr_rate_type_nm": o.get("intr_rate_type_nm"),
            "rsrv_type_nm": o.get("rsrv_type_nm"),
            "join_deny": o.get("product__join_deny"),
        }
        for o in ranked
    ]

# 상품별 텍스트(우대조건/유의사항/만기 후 이자 등)를 상품 단위로 한 번만 모아서 payload에 넣음 
def _build_product_texts(product_ids: List[int]) -> Dict[int, Dict[str, Any]]:
    """
    Top10 상품의 텍스트/메타를 상품 단위로 1번만 모아서 제공.
    candidates에 텍스트를 중복 포함시키지 않아 payload 폭증을 방지한다.
    """
    qs = (
        Product.objects
        .select_related("bank")
        .filter(id__in=product_ids)
        .values(
            "id",
            "fin_prdt_nm",
            "product_type",
            "join_deny",
            "spcl_cnd",
            "etc_note",
            "mtrt_int",
            "bank__kor_co_nm",
        )
    )
    out: Dict[int, Dict[str, Any]] = {}
    for p in qs:
        pid = int(p["id"])
        out[pid] = {
            "product_name": p.get("fin_prdt_nm"),
            "bank_name": p.get("bank__kor_co_nm"),
            "product_type": p.get("product_type"),
            "join_deny": p.get("join_deny"),
            "spcl_cnd": p.get("spcl_cnd"),
            "etc_note": p.get("etc_note"),
            "mtrt_int": p.get("mtrt_int"),
        }
    return out

# LLM 응답에서 JSON 객체 추출하고 파싱 
def _extract_json(text: str) -> Dict[str, Any]:
    t = (text or "").strip()

    # ```json ... ``` 제거
    if t.startswith("```"):
        t = t.strip("`").strip()
        if t.lower().startswith("json"):
            t = t[4:].strip()

    l = t.find("{")
    r = t.rfind("}")
    if l == -1 or r == -1 or r <= l:
        raise ValueError("JSON 파싱 실패")
    return json.loads(t[l:r + 1])

# GMS 호출 
def _gms_chat_completion_json(
    *,
    model: str,
    payload_obj: Dict[str, Any],
    timeout_sec: int = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    api_key = os.getenv("GMS_KEY")
    if not api_key:
        raise RuntimeError("GMS_KEY를 찾지 못했습니다. backend/.env에 GMS_KEY=... 확인하세요.")

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    body = {
        "model": model,
        "messages": [
            {"role": "developer", "content": DEVELOPER_MSG},
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": json.dumps(payload_obj, ensure_ascii=False)},
        ],
    }

    r = requests.post(GMS_URL, headers=headers, json=body, timeout=timeout_sec)

    # 실패 원인을 굳이 사용자 응답에 섞지 않더라도, 내부 예외로는 명확히 처리
    data = r.json()
    if r.status_code >= 400:
        raise ValueError("GMS request failed")

    content = data["choices"][0]["message"]["content"]
    return _extract_json(content)

# Stage1에서 받은 결과에서 최종 option_id 1개 확정 
def pick_final_option_from_top10(
    *,
    user,
    goal: Dict[str, Any],
    top10_products: List[Dict[str, Any]],
    model: str | None = None,
    per_product_candidates: int = 3,
) -> Stage2Output:
    model = DEFAULT_MODEL

    goal_ctx = _goal_ctx(goal)
    top10_ids = [int(x["product_id"]) for x in top10_products[:10]]

    candidates: List[Dict[str, Any]] = []
    for pid in top10_ids:
        candidates.extend(
            shortlist_options_for_product(
                pid,
                term_months=int(goal_ctx["term_months"]),
                per_product=per_product_candidates,
            )
        )
    if not candidates:
        raise ValueError("Top10 상품들에서 선택 가능한 옵션 후보를 찾지 못했습니다.")

    valid_product_ids = set(top10_ids)
    valid_option_ids = {int(c["option_id"]) for c in candidates}

    product_texts = _build_product_texts(top10_ids)

    payload = {
        "user": _user_ctx(user),
        "goal": goal_ctx,
        "top10_product_ids": top10_ids,
        "top10_products_with_scores": top10_products[:10],
        "candidates": candidates,
        "product_texts": product_texts,  # ✅ spcl_cnd / etc_note 포함(상품 단위)
    }

    try:
        out = _gms_chat_completion_json(model=model, payload_obj=payload)

        product_id = int(out["product_id"])
        option_id = int(out["option_id"])

        reasons = out.get("reasons", [])
        warnings = out.get("warnings", [])

        # 리스트 형태 강제 + 최소 요건 보정(불필요한 fallback 유발 방지)
        if not isinstance(reasons, list):
            reasons = []
        reasons = [str(x).strip() for x in reasons if str(x).strip()]
        if len(reasons) < 2:
            reasons = ["목표 기간과 옵션 기간의 적합도를 우선했습니다.", "금리 기준으로 동점일 때 우선순위를 적용했습니다."]
        reasons = reasons[:5]

        if not isinstance(warnings, list):
            warnings = []
        warnings = [str(x).strip() for x in warnings if str(x).strip()]
        warnings = warnings[:4]

        # 핵심 검증(이탈 시 fallback)
        if product_id not in valid_product_ids:
            raise ValueError("invalid product_id")
        if option_id not in valid_option_ids:
            raise ValueError("invalid option_id")

        return Stage2Output(
            product_id=product_id,
            option_id=option_id,
            reasons=reasons,
            warnings=warnings,
            used_fallback=False,
        )

    except Exception:
        best_pid = int(top10_products[0]["product_id"])
        fb = shortlist_options_for_product(
            best_pid,
            term_months=int(goal_ctx["term_months"]),
            per_product=1,
        )

        if fb:
            chosen = fb[0]
            term = int(goal_ctx["term_months"])
            save_trm = int(chosen.get("save_trm"))
            term_gap = abs(save_trm - term)

            rate2 = chosen.get("intr_rate2")
            rate = chosen.get("intr_rate")
            rate_used = rate2 if rate2 is not None else rate

            reasons = [
                f"목표 기간 {term}개월에 가장 근접한 옵션(저축기간 {save_trm}개월, 차이 {term_gap}개월)을 선택했습니다.",
            ]
            if rate_used is not None:
                reasons.append(
                    f"후보 중 금리 우선순위(우대금리→기본금리) 기준에서 유리한 값을 고려했습니다. (적용 금리: {rate_used}%)"
                )

            warnings = []
            # join_deny가 있으면 사용자에게 의미 있는 경고만 남김
            jd = chosen.get("join_deny")
            if jd not in (None, "", "0"):
                warnings.append(f"가입 제한(join_deny={jd})이 있을 수 있어 가입 조건 확인이 필요합니다.")

            return Stage2Output(
                product_id=best_pid,
                option_id=int(chosen["option_id"]),
                reasons=reasons[:5] if reasons else ["목표 기간 적합도를 우선해 옵션을 선택했습니다."],
                warnings=warnings[:4],
                used_fallback=True,
            )

        first = candidates[0]
        return Stage2Output(
            product_id=int(first["product_id"]),
            option_id=int(first["option_id"]),
            reasons=["후보 옵션 중 조건 충족이 확인된 옵션을 선택했습니다."],
            warnings=[], 
            used_fallback=True,
        )