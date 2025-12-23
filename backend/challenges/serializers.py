from django.db.models import Count
from rest_framework import serializers
from .models import Moathon, MoathonComment
from products.serializers import ProductOptionSimpleSerializer
from datetime import date

from accounts.models import UserBadge, UserFollow 

# 단일 모아톤 조회
class MoathonDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    profile_image = serializers.ImageField(source='user.profile_image', read_only=True)

    product_option = ProductOptionSimpleSerializer(read_only=True)
    progress_rate = serializers.SerializerMethodField()

    # 작성자의 획득한 뱃지 리스트
    owner_badges = serializers.SerializerMethodField()

    # 작성자의 팔로워/팔로잉 수 + 내가 팔로우 중인지
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Moathon
        fields = [
            'id', 'title', 'purpose', 'progress_rate', 'target_amount', 'start_date', 'end_date',
            'product_option',
            'nickname', 'profile_image',
            'follower_count', 'following_count', 'is_following',
            'owner_badges',
        ]

    def get_progress_rate(self, obj):
        total_days = (obj.end_date - obj.start_date).days
        elapsed_days = (date.today() - obj.start_date).days

        if total_days <= 0: return 100
        if elapsed_days <= 0: return 0

        rate = (elapsed_days / total_days) * 100
        return min(int(rate), 100)

    def get_follower_count(self, obj):
        owner = obj.user
        return UserFollow.objects.filter(following=owner).count()

    def get_following_count(self, obj):
        owner = obj.user
        return UserFollow.objects.filter(follower=owner).count()

    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        me = request.user
        owner = obj.user
        if me.id == owner.id:
            return False

        return UserFollow.objects.filter(follower=me, following=owner).exists()

    def get_owner_badges(self, obj):
        owner = obj.user
        qs = (
            UserBadge.objects
            .filter(user=owner)
            .select_related("badge", "moathon")
            .order_by("-obtained_at")
        )

        return [
            {
                "id": ub.badge_id,
                "type": ub.badge.type,
                "name": ub.badge.name,
                "description": ub.badge.description,
                "url": ub.badge.badge_url,
                "moathon_id": ub.moathon_id,  # track이면 값 존재 가능
                "obtained_at": ub.obtained_at,
            }
            for ub in qs
        ]

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

# 모아톤 댓글 
class MoathonCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = MoathonComment
        fields = ["id", "moathon", "content", "nickname", "created_at", "updated_at"]
        read_only_fields = ["id", "moathon", "nickname", "created_at", "updated_at"]

# 댓글 작성/수정
class MoathonCommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoathonComment
        fields = ["content"]

    def validate_content(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("댓글 내용은 비어 있을 수 없습니다.")
        if len(value) > 500:
            raise serializers.ValidationError("댓글은 최대 500자까지 작성할 수 있습니다.")
        return value