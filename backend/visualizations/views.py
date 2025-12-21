from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import CommodityPriceQuerySerializer
from .models import CommodityAsset, CommodityPrice


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
