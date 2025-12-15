from django.db import models
from django.conf import settings
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
        through='accounts.Moathon',
        blank=True,
        related_name="subscribed_users",  # Product 입장에서 "이 상품 가입한 유저들"
    )


class Moathon(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users_moathon",
    )
    product_option = models.ForeignKey(
        "products.ProductOption",
        on_delete=models.CASCADE,
        related_name="moathons",
    )

    title = models.CharField(max_length=50, blank=True, default="")
    target_amount = models.PositiveBigIntegerField()      # 목표 금액(원)
    start_amount = models.PositiveBigIntegerField()       # 시작 금액(원)
    term_months = models.PositiveSmallIntegerField()      # 목표 기간(개월)
    PURPOSE = (
        ("GOAL", "목돈 마련"),
        ("SHORT", "단기 여유자금"),
        ("SAFE", "안정적 자산 보관"),
        ("HABIT", "저축 습관 형성"),
        ("YIELD", "이자 극대화"),
    )
    purpose = models.CharField(max_length=10, choices=PURPOSE)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "title"], name="uniq_moathon_title_per_user"),
        ]

    DEFAULT_TITLE_BASE = "user's moathon"

    def _next_default_title(self) -> str:
        base = self.DEFAULT_TITLE_BASE

        titles = (Moathon.objects
                  .filter(user=self.user, title__startswith=base)
                  .values_list("title", flat=True))

        max_n = 0
        for t in titles:
            if t == base:
                max_n = max(max_n, 1)
                continue
            suffix = t[len(base):]
            if suffix.isdigit():
                max_n = max(max_n, int(suffix))

        return base if max_n == 0 else f"{base}{max_n + 1}"

    def save(self, *args, **kwargs):
        if not self.pk and not (self.title or "").strip():
            self.title = self._next_default_title()
        super().save(*args, **kwargs)