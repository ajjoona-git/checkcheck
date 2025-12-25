from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import CommodityPriceQuerySerializer
from .models import CommodityAsset, CommodityPrice

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# 금/은 시세
def serialize_prices(qs):
    out = []
    for p in qs:
        out.append({
            "date": p.date.isoformat(),
            "close_last": float(p.close_last),
            "open": float(p.open),
            "high": float(p.high),
            "low": float(p.low),
            "volume": int(p.volume) if p.volume is not None else None,
        })
    return out

# 원자재 가격 시계열 내역 조회
@extend_schema(
    tags=["Visualizations"],
    summary="원자재 가격 시계열 조회",
    description=(
        "asset(gold/silver 등)를 기준으로 원자재 가격 시계열 데이터를 반환합니다. "
        "start/end를 둘 다 주면 해당 기간만 필터링합니다."
    ),
    parameters=[
        OpenApiParameter(
            name="asset",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            required=True,
            description="조회할 asset 코드 (예: gold, silver). 존재 여부는 서버에서 검증합니다.",
        ),
        OpenApiParameter(
            name="start",
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            required=False,
            description="시작일(YYYY-MM-DD). end와 함께 입력해야 합니다.",
        ),
        OpenApiParameter(
            name="end",
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            required=False,
            description="종료일(YYYY-MM-DD). start와 함께 입력해야 합니다.",
        ),
    ],
    responses={
        200: OpenApiTypes.OBJECT,
        400: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            "요청 예시(전체 기간)",
            value={"asset": "gold"},
            request_only=True,
        ),
        OpenApiExample(
            "요청 예시(기간 필터)",
            value={"asset": "gold", "start": "2024-01-01", "end": "2024-12-31"},
            request_only=True,
        ),
        OpenApiExample(
            "응답 예시(데이터 있음)",
            value={
                "asset": "gold",
                "start": "2024-01-01",
                "end": "2024-12-31",
                "count": 2,
                "data": [
                    {
                        "date": "2024-01-02",
                        "close_last": 2050.1,
                        "open": 2042.3,
                        "high": 2061.5,
                        "low": 2038.9,
                        "volume": 123456,
                    },
                    {
                        "date": "2024-01-03",
                        "close_last": 2060.4,
                        "open": 2051.0,
                        "high": 2068.2,
                        "low": 2047.7,
                        "volume": None,
                    },
                ],
            },
            response_only=True,
        ),
        OpenApiExample(
            "응답 예시(데이터 없음)",
            value={
                "asset": "gold",
                "start": "2024-01-01",
                "end": "2024-01-02",
                "count": 0,
                "message": "해당 기간에 해당하는 데이터가 없습니다.",
                "data": [],
            },
            response_only=True,
        ),
        OpenApiExample(
            "응답 예시(400 - 파라미터 오류)",
            value={
                "message": "요청 파라미터가 올바르지 않습니다.",
                "errors": {"end": ["기간 선택 시 시작일과 종료일을 모두 입력해주세요."]},
            },
            response_only=True,
        ),
    ],
)
@api_view(["GET"])
def commodity_price_series(request):
    q = CommodityPriceQuerySerializer(data=request.query_params)
    if not q.is_valid():
        return Response(
            {"message": "요청 파라미터가 올바르지 않습니다.", "errors": q.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    asset_code = q.validated_data["asset"]
    start = q.validated_data.get("start")
    end = q.validated_data.get("end")

    # 존재 검증은 serializer에서 했지만, get은 여기서 수행
    asset_obj = CommodityAsset.objects.get(asset=asset_code)

    # 기간 입력없으면 전체
    qs = (
        CommodityPrice.objects
        .filter(commodity=asset_obj)
        .only("date", "close_last", "open", "high", "low", "volume")
        .order_by("date")
    )

    # 기간 입력 있다면 filter
    if start and end:
        qs = qs.filter(date__range=(start, end))

    if not qs.exists():
        return Response(
            {
                "asset": asset_code,
                "start": start.isoformat() if start else None,
                "end": end.isoformat() if end else None,
                "count": 0,
                "message": "해당 기간에 해당하는 데이터가 없습니다.",
                "data": [],
            },
            status=status.HTTP_200_OK,
        )

    data = serialize_prices(qs)
    return Response(
        {
            "asset": asset_code,
            "start": start.isoformat() if start else None,
            "end": end.isoformat() if end else None,
            "count": len(data),
            "data": data,
        },
        status=status.HTTP_200_OK,
    )
