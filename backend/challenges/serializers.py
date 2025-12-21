from rest_framework import serializers
from .models import Moathon
from products.models import ProductOption
from products.serializers import ProductOptionSerializer
from datetime import date

# 단일 모아톤 조회
class MoathonDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    profile_image = serializers.ImageField(source='user.profile_image', read_only=True)
    # 뱃지 로직이 있다면 source='user.badge' 등으로 추가
    
    # Nested Serializer: ProductOption의 상세 정보를 한 번에 보여줌
    product_option = ProductOptionSerializer(read_only=True)
    progress_rate = serializers.SerializerMethodField()

    class Meta:
        model = Moathon
        fields = [
            'id', 'title', 'purpose', 'progress_rate', 'target_amount', 'start_date', 'end_date',
            'product_option',
            'nickname', 'profile_image'
        ]

    def get_progress_rate(self, obj):
        # 공식: (오늘 - 시작일) / (종료일 - 시작일) * 100
        total_days = (obj.end_date - obj.start_date).days
        elapsed_days = (date.today() - obj.start_date).days
        
        if total_days <= 0: return 100
        if elapsed_days <= 0: return 0

        rate = (elapsed_days / total_days) * 100
        return min(int(rate), 100)

# 전체 모아톤 조회
class MoathonListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    bank = serializers.CharField(source='product_option.product.bank.kor_co_nm', read_only=True)
    product_name = serializers.CharField(source='product_option.product.fin_prdt_nm', read_only=True)
    progress_rate = serializers.SerializerMethodField()    

    class Meta:
        model = Moathon
        fields = ['id', 'title', 'nickname', 'bank', 'product_name', 'progress_rate']

    def get_progress_rate(self, obj):
        # 공식: (오늘 - 시작일) / (종료일 - 시작일) * 100
        total_days = (obj.end_date - obj.start_date).days
        elapsed_days = (date.today() - obj.start_date).days
        
        if total_days <= 0: return 100
        if elapsed_days <= 0: return 0
        
        rate = (elapsed_days / total_days) * 100
        return min(int(rate), 100)

# 모아톤 생성하기
class MoathonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moathon
        fields = ['title', 'target_amount', 'start_amount', 'purpose', 'product_option']

    def validate(self, data):
        if data['start_amount'] > data['target_amount']:
            raise serializers.ValidationError("시작 금액이 목표 금액보다 클 수 없습니다.")
        return data
    
# 모아톤 수정하기
class MoathonUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moathon
        fields = ['title', 'target_amount', 'purpose']