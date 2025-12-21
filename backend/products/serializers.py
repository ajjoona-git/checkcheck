from rest_framework import serializers
from .models import Product, ProductOption

class ProductOptionSerializer(serializers.ModelSerializer):
    fin_prdt_nm = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    product_type = serializers.CharField(source='product.product_type', read_only=True)
    kor_co_nm = serializers.CharField(source='product.bank.kor_co_nm', read_only=True)

    class Meta:
        model = ProductOption
        fields = [
            'id',
            'fin_prdt_nm',   # 상품명
            'kor_co_nm',     # 은행명
            'product_type',  # 예금/적금 구분
        ]