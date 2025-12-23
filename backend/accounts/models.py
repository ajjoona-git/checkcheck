from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from challenges.models import Moathon
from django.db.models import Q

# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True) # 필수: 닉네임
    birth = models.DateField(max_length=100) # 필수: 생년월일
    # 나중에 입력 가능: 프로필 이미지
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )
    # 나중에 입력 가능: 성별
    GENDER_CHOICES = (
        ("0", "남성"),
        ("1", "여성"),
    )
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True)
    credit_score = models.PositiveIntegerField(blank=True, null=True) # 나중에 입력 가능: 신용점수
    assets = models.PositiveBigIntegerField(blank=True, null=True) # 나중에 입력 가능: 자산(원 단위)
    salary = models.PositiveIntegerField(blank=True, null=True) # 나중에 입력 가능: 연봉
    average_monthly_spend = models.PositiveIntegerField(blank=True, null=True) # 나중에 입력 가능: 평균 월 지출
    # 나중에 입력 가능: 투자 성향
    TENDER_CHOICES = (
        ("1", "매우보수적"),
        ("2", "보수적"),
        ("3", "보통"),
        ("4", "공격적"),
        ("5", "매우공격적"),
    )
    tender = models.CharField(choices=TENDER_CHOICES, blank=True, null=True)
    # 가입한 금융상품 목록
    products = models.ManyToManyField(
        "products.ProductOption",
        through='challenges.Moathon',
        blank=True,
        related_name="subscribed_users",  # Product 입장에서 "이 상품 가입한 유저들"
    )

class Badge(models.Model):
    # 뱃지 타입 구분 (track, achieve, social)
    type = models.CharField(max_length=20)
    # 뱃지 이름
    name = models.CharField(max_length=20)
    # 뱃지 설명 및 획득 조건
    description = models.CharField()
    # ex) frontend/src/assets/badges/badge_achieve_3dats.png
    badge_url = models.CharField()


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    # [핵심] 트랙 뱃지인 경우, 어떤 모아톤에서 획득했는지 연결
    # 일반 뱃지(팔로워 10명 등)인 경우 null=True
    moathon = models.ForeignKey(Moathon, on_delete=models.CASCADE, null=True, blank=True)

    obtained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # 같은 모아톤에서 같은 뱃지(예: 50% 뱃지)를 중복해서 받을 수 없음
            # 하지만 다른 모아톤에서는 같은 50% 뱃지를 또 받을 수 있음! (이게 중요)
            models.UniqueConstraint(
                fields=['user', 'badge', 'moathon'],
                name='unique_badge_per_moathon'
            ),
            # 유저 종속(모아톤이 없는) 뱃지는 유저당 1번만
            models.UniqueConstraint(
                fields=["user", "badge"],
                condition=Q(moathon__isnull=True),
                name="unique_user_badge_when_moathon_null",
            ),
        ]

class UserFollow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following_relations",
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follower_relations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow_pair",
            )
        ]
        indexes = [
            models.Index(fields=["following", "created_at"]),
            models.Index(fields=["follower", "created_at"]),
        ]