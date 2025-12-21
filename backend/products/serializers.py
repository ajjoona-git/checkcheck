from rest_framework import serializers
from .models import Product, ProductOption

# 모아톤 상세 페이지에 사용할 금융 상품 정보
class ProductOptionSimpleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    product_type = serializers.CharField(source='product.product_type', read_only=True)
    bank_name = serializers.CharField(source='product.bank.kor_co_nm', read_only=True)

    class Meta:
        model = ProductOption
        fields = [
            'id',
            'product_name',   # 상품명
            'bank_name',     # 은행명
            'product_type',  # 예금/적금 구분
        ]