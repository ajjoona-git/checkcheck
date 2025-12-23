from rest_framework import serializers
from .models import Product, ProductOption, Bank

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

# 금융 상품 전체 조회
class ProductListSerializer(serializers.ModelSerializer):
    class ProductOptionSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductOption
            fields = [
                'id',
                'save_trm',
                'intr_rate',
                'intr_rate2'
            ]

    options = ProductOptionSerializer(many=True, read_only=True)
    bank_name = serializers.CharField(source='bank.kor_co_nm', read_only=True)
    max_rate = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'dcls_month',
            'bank_name',
            'product_type',
            'fin_prdt_nm',
            'join_way',
            'options',
            'max_rate',
        ]

    # 해당 상품의 옵션 중 가장 높은 우대금리를 계산해서 반환
    def get_max_rate(self, obj):
        options = obj.options.all()
        if not options:
            return None
        rates = [opt.intr_rate2 for opt in options if opt.intr_rate2 is not None]
        return max(rates) if rates else None

# 금융 상품 상세 조회
class ProductDetailSerializer(serializers.ModelSerializer):
    class ProductOptionSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductOption
            fields = '__all__'

    options = ProductOptionSerializer(many=True, read_only=True)
    bank_name = serializers.CharField(source='bank.kor_co_nm', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'