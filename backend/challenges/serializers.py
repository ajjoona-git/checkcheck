from django.db.models import Count
from rest_framework import serializers
from .models import Moathon, MoathonComment, MoathonLike
from products.serializers import ProductOptionSimpleSerializer
from datetime import date

from accounts.models import UserBadge, UserFollow

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
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = MoathonComment
        fields = ["id", "moathon", "content", "nickname", 'is_owner', "created_at", "updated_at"]
        read_only_fields = ["id", "moathon", "nickname", 'is_owner', "created_at", "updated_at"]

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request and request.user == obj.user

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
    
# 단일 모아톤 조회
class MoathonDetailSerializer(serializers.ModelSerializer):
    product_option = ProductOptionSimpleSerializer(read_only=True)
    progress_rate = serializers.SerializerMethodField()

    user_info = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = MoathonCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Moathon
        fields = [
            'id', 'title', 'purpose', 'progress_rate', 'target_amount', 'start_date', 'end_date',
            'product_option',
            'user_info',  # 유저 정보 그룹
            'likes',      # 좋아요 정보 그룹
            'comments',   # 댓글 리스트
        ]

    def get_progress_rate(self, obj):
        total_days = (obj.end_date - obj.start_date).days
        elapsed_days = (date.today() - obj.start_date).days

        if total_days <= 0: return 100
        if elapsed_days <= 0: return 0

        rate = (elapsed_days / total_days) * 100
        return min(int(rate), 100)

    def get_user_info(self, obj):
        owner = obj.user
        request = self.context.get("request")
        
        # 1) 팔로워/팔로잉 카운트
        follower_count = UserFollow.objects.filter(following=owner).count()
        following_count = UserFollow.objects.filter(follower=owner).count()
        
        # 2) 내가 팔로우 중인지 확인
        is_following = False
        if request and request.user.is_authenticated and request.user.id != owner.id:
            is_following = UserFollow.objects.filter(follower=request.user, following=owner).exists()

        # 3) 뱃지 리스트
        badges_qs = (
            UserBadge.objects
            .filter(user=owner)
            .select_related("badge")
            .order_by("-obtained_at")
        )
        owner_badges = [
            {
                "id": ub.badge.id,
                "type": ub.badge.type,
                "name": ub.badge.name,
                "description": ub.badge.description,
                "url": ub.badge.badge_url,
                "obtained_at": ub.obtained_at,
            }
            for ub in badges_qs
        ]

        # 4) 프로필 이미지 URL 처리
        profile_image_url = None
        if owner.profile_image:
            try:
                profile_image_url = request.build_absolute_uri(owner.profile_image.url)
            except:
                profile_image_url = owner.profile_image.url

        return {
            "nickname": owner.nickname,
            "profile_image": profile_image_url,
            "follower_count": follower_count,
            "following_count": following_count,
            "is_following": is_following,
            "owner_badges": owner_badges
        }

    def get_likes(self, obj):
        request = self.context.get("request")
        count = MoathonLike.objects.filter(moathon=obj).count()
        
        is_liked = False
        if request and request.user.is_authenticated:
            is_liked = MoathonLike.objects.filter(moathon=obj, user=request.user).exists()
            
        return {
            "count": count,
            "is_liked": is_liked
        }