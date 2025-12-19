from django.db import models
from django.contrib.auth.models import AbstractUser

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
