from rest_framework import serializers
from .models import CommodityAsset
from datetime import date
from typing import Optional

# 원자재 가격 시계열 조회 시리얼라이저
class CommodityPriceQuerySerializer(serializers.Serializer):
    asset = serializers.CharField(required=True)  # 'gold'/'silver'
    start = serializers.DateField(required=False)  # YYYY-MM-DD
    end = serializers.DateField(required=False)    # YYYY-MM-DD

    def validate_asset(self, value):
        value = value.strip().lower()
        if not CommodityAsset.objects.filter(asset=value).exists():
            raise serializers.ValidationError("존재하지 않는 asset 입니다.")
        return value

    def validate(self, attrs):
        start: Optional[date] = attrs.get("start")
        end: Optional[date] = attrs.get("end")

        # 기간 선택 시 둘 다 입력
        if (start and not end) or (end and not start):
            raise serializers.ValidationError("기간 선택 시 시작일과 종료일을 모두 입력해주세요.")

        if start and end and start > end:
            raise serializers.ValidationError("시작일은 종료일보다 이후일 수 없습니다.")
        return attrs
