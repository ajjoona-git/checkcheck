from __future__ import annotations
from typing import Any, Dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from products.models import ProductOption, Product
from .serializers import RecommendationPreviewSerializer
from .services.stage1_inference import stage1_recommend_topk_products
from .services.stage2_openai import pick_final_option_from_top10

# 선택된 상품의 디테일한 옵션 생성
def _build_final_option_detail(option_id: int) -> Dict[str, Any]:
    opt = (
        ProductOption.objects
        .select_related("product", "product__bank")
        .filter(id=int(option_id))
        .first()
    )
    if not opt:
        return {"option_id": int(option_id)}

    p = opt.product
    return {
        "option_id": int(opt.id),
        "product_id": int(opt.product_id),
        "product_name": p.fin_prdt_nm, # 금융 상품명
        "bank_name": p.bank.kor_co_nm, # 은행명
        "product_type": p.product_type, # 정기예금/적금
        "join_deny": p.join_deny, # 가입제한
        "max_limit": p.max_limit, # 최고 한도 
        "save_trm": opt.save_trm, # 저축기간 
        "intr_rate": opt.intr_rate, # 기본금리
        "intr_rate2": opt.intr_rate2, # 최고우대금리 
        "rsrv_type_nm": opt.rsrv_type_nm, # 적립유형(정액정립식/자유적립식/None(정기예금일 경우))
        "intr_rate_type_nm": opt.intr_rate_type_nm, # 금리유형명(단리/복리)
        "spcl_cnd": p.spcl_cnd, # 우대조건
        "etc_note": p.etc_note, # 기타유의사항
        "mtrt_int": p.mtrt_int, # 만기 후 이자율 
    }


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def recommend_product(request):
    ser = RecommendationPreviewSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    v = ser.validated_data

    goal = {
        "target_amount": int(v["target_amount"]),
        "start_amount": int(v["start_amount"]),
        "term_months": int(v["term_months"]),
        "purpose": v["purpose"],
    }

    # XGB 모델로 1차 상품 10개 추천 
    topk = stage1_recommend_topk_products(
        user=request.user,
        goal=goal,
        top_k=int(v.get("top_k", 10)),
    )

    top10 = topk[:10]

    # LLM 모델로 최종 상품 옵션 한가지 추천 
    final = pick_final_option_from_top10(
        user=request.user,
        goal=goal,
        top10_products=top10,
        per_product_candidates=int(v.get("per_product_candidates", 3)),
    )

    final_option_detail = _build_final_option_detail(final.option_id)

    resp = {
        "final_recommendation": { # 프론트에서 사용자에게 추천된 상품으로 보여줄 값 
            "product_id": final.product_id,
            "option_id": final.option_id, 
            "reasons": final.reasons, # Stage2에서 분석된 해당 상품 옵션을 선택한 이유
            "warnings": final.warnings, # Stage2에서 분석된 해당 상품의 주의사항
            "used_fallback": final.used_fallback, # GMS 모델 답변인지 / 규칙기반 답변인지
            "option_detail": final_option_detail, # 위에서 정의한 선택한 상품 옵션 디테일 묶음
        },
        "confirm_payload": { # 해당 상품을 선택할 때 Moathon테이블의 필드로 저장할 값 
            "product_option_id": final.option_id,
            "target_amount": goal["target_amount"],
            "start_amount": goal["start_amount"],
            "term_months": goal["term_months"],
            "purpose": goal["purpose"],
        },
    }

    return Response(resp, status=status.HTTP_200_OK)
