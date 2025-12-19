from __future__ import annotations
import joblib
import pandas as pd
from pathlib import Path
from django.utils import timezone

from products.models import ProductOption  # FK로 ProductModel 탐색용

ART_DIR = Path(__file__).resolve().parents[1]

# Lazy Load로 변경하여 migrations 시점에 터지지 않도록 함.
_PIPE = None
_SPEC = None
_CAT_COLS = None
_NUM_COLS = None

def get_stage1_assets():
    global _PIPE, _SPEC, _CAT_COLS, _NUM_COLS

    if _PIPE is not None:
        return _PIPE, _CAT_COLS, _NUM_COLS

    pipe_path = ART_DIR / "stage1_pipe.joblib"
    spec_path = ART_DIR / "stage1_feature_spec.joblib"

    if not pipe_path.exists() or not spec_path.exists():
        return None, None, None

    _PIPE = joblib.load(pipe_path)
    _SPEC = joblib.load(spec_path)
    _CAT_COLS = _SPEC["cat_cols"]
    _NUM_COLS = _SPEC["num_cols"]
    return _PIPE, _CAT_COLS, _NUM_COLS

# ProductModel 탐색
product_fk = ProductOption._meta.get_field("product")
ProductModel = product_fk.related_model


def build_product_agg_from_options() -> pd.DataFrame:
    all_fields = {f.name for f in ProductOption._meta.fields}

    fields = ["product_id"]
    cand_fields = ["intr_rate", "intr_rate2", "save_trm", "rsrv_type_nm", "intr_rate_type_nm"]
    fields += [c for c in cand_fields if c in all_fields]

    qs = ProductOption.objects.values(*fields)
    opt = pd.DataFrame(list(qs))

    if opt.empty:
        return pd.DataFrame(columns=["product_id"])

    # save_trm은 CharField -> 숫자 변환해서 집계(문자열 min/max 방지)
    if "save_trm" in opt.columns:
        opt["save_trm_num"] = pd.to_numeric(opt["save_trm"], errors="coerce")

    agg_dict = {}

    # 금리 집계
    if "intr_rate2" in opt.columns:
        agg_dict["prod_max_intr_rate2"] = ("intr_rate2", "max")
        agg_dict["prod_mean_intr_rate2"] = ("intr_rate2", "mean")
    if "intr_rate" in opt.columns:
        agg_dict["prod_max_intr_rate"] = ("intr_rate", "max")
        agg_dict["prod_mean_intr_rate"] = ("intr_rate", "mean")

    # 기간/옵션 수 집계
    if "save_trm" in opt.columns:
        agg_dict["prod_min_save_trm"] = ("save_trm_num", "min")
        agg_dict["prod_max_save_trm"] = ("save_trm_num", "max")
        agg_dict["prod_cnt_options"] = ("save_trm_num", "count")

    # 기본 agg
    if agg_dict:
        agg = opt.groupby("product_id", as_index=False).agg(**agg_dict)
    else:
        agg = opt[["product_id"]].drop_duplicates().copy()

    # 적립유형 플래그 (rsrv_type_nm 기준)
    if "rsrv_type_nm" in opt.columns:
        def _has_contains(series: pd.Series, keyword: str) -> int:
            s = series.fillna("").astype(str)
            return int(s.str.contains(keyword).any())

        rsrv_flags = opt.groupby("product_id")["rsrv_type_nm"].apply(
            lambda s: pd.Series({
                "has_rsrv_free": _has_contains(s, "자유"),   # "자유적립식" 등
                "has_rsrv_fixed": _has_contains(s, "정액"),  # "정액적립식" 등
            })
        ).reset_index()

        agg = agg.merge(rsrv_flags, on="product_id", how="left")
    else:
        agg["has_rsrv_free"] = 0
        agg["has_rsrv_fixed"] = 0

    # 금리유형 플래그 (intr_rate_type_nm: 단리/복리)
    if "intr_rate_type_nm" in opt.columns:
        def _has_type(series: pd.Series, keyword: str) -> int:
            s = series.fillna("").astype(str)
            return int(s.str.contains(keyword).any())

        intr_type_flags = opt.groupby("product_id")["intr_rate_type_nm"].apply(
            lambda s: pd.Series({
                "has_simple_interest": _has_type(s, "단리"),
                "has_compound_interest": _has_type(s, "복리"),
            })
        ).reset_index()

        agg = agg.merge(intr_type_flags, on="product_id", how="left")
    else:
        agg["has_simple_interest"] = 0
        agg["has_compound_interest"] = 0

    # 플래그 NaN -> 0
    for c in ["has_rsrv_free", "has_rsrv_fixed", "has_simple_interest", "has_compound_interest"]:
        if c in agg.columns:
            agg[c] = agg[c].fillna(0).astype(int)

    return agg


def build_user_goal_row(user, goal: dict) -> pd.DataFrame:
    today = timezone.now().date()
    age = (today - user.birth).days // 365 if getattr(user, "birth", None) else None

    salary = user.salary or 0
    avg_spend = user.average_monthly_spend or 0
    annual_spend = avg_spend * 12
    disposable = salary - annual_spend
    spend_ratio = annual_spend / (salary if salary != 0 else 1)

    target_amount = int(goal["target_amount"])
    start_amount = int(goal["start_amount"])
    term_months = int(goal["term_months"])
    need_amount = max(target_amount - start_amount, 0)
    need_per_month = need_amount / (term_months or 1)

    row = {
        "age": age,
        "gender": user.gender,
        "credit_score": user.credit_score,
        "assets": user.assets,
        "salary": salary,
        "average_monthly_spend": avg_spend,
        "tender": user.tender,
        "annual_spend": annual_spend,
        "disposable": disposable,
        "spend_ratio": spend_ratio,
        "term_months": term_months,
        "purpose": goal["purpose"],
        "target_amount": target_amount,
        "start_amount": start_amount,
        "need_amount": need_amount,
        "need_per_month": need_per_month,
    }
    return pd.DataFrame([row])


def stage1_recommend_topk_products(user, goal: dict, top_k: int = 10) -> list[dict]:
    PIPE, CAT_COLS, NUM_COLS = get_stage1_assets()
    if PIPE is None:
        raise RuntimeError("Stage1 joblib( stage1_pipe.joblib / stage1_feature_spec.joblib )가 아직 없습니다. 학습 후 생성하세요.")

    user_goal = build_user_goal_row(user, goal)

    # 후보 상품
    prod_ids = list(ProductModel.objects.values_list("id", flat=True))
    cand = pd.DataFrame({"product_id": prod_ids})

    prod_agg = build_product_agg_from_options()
    cand = cand.merge(prod_agg, on="product_id", how="left")

    # cross join
    user_goal["key"] = 1
    cand["key"] = 1
    pair = user_goal.merge(cand, on="key").drop(columns=["key"])

    # 학습 때 사용한 컬럼만 정확히 구성
    X = pair[CAT_COLS + NUM_COLS]
    scores = PIPE.predict_proba(X)[:, 1]

    out = pd.DataFrame({"product_id": pair["product_id"].astype(int), "score": scores})

    # product_id 중복 제거: 같은 product_id면 score 최댓값만 남김
    out = out.groupby("product_id", as_index=False)["score"].max()

    out = out.sort_values("score", ascending=False).head(top_k)
    return out.to_dict(orient="records")