from django.db import models
from django.conf import settings
from datetime import date, timedelta

# Create your models here.
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

    start_date = models.DateField(default=date.today)     # 시작일 (오늘 날짜로 자동 생성)
    end_date = models.DateField()                         # 만기일 (ProductOption의 기간을 더해서 계산)

    PURPOSE = (
        ("GOAL", "목돈 마련"),
        ("SHORT", "단기 여유자금"),
        ("SAFE", "안정적 자산 보관"),
        ("HABIT", "저축 습관 형성"),
        ("YIELD", "이자 극대화"),
    )
    purpose = models.CharField(max_length=10, choices=PURPOSE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "title"], name="uniq_moathon_title_per_user"),
        ]

    DEFAULT_TITLE_BASE = f"{user}\'s moathon"

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
        if not self.pk:
            if not (self.title or "").strip():
                self.title = self._next_default_title()
            
            if not self.start_date:
                self.start_date = date.today()
            
            if self.product_option and self.product_option.save_trm:
                try:
                    months = int(self.product_option.save_trm)
                except (ValueError, TypeError):
                    months = 12
                days = months * 30
                self.end_date = self.start_date + timedelta(days=days)
            else:
                self.end_date = self.start_date + timedelta(days=365)

        super().save(*args, **kwargs)

class MoathonComment(models.Model):
    moathon = models.ForeignKey(
        "challenges.Moathon",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="moathon_comments",
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 최신순 댓글 정렬 
    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["moathon", "created_at"]),
        ]

class MoathonLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="moathon_likes",
    )
    moathon = models.ForeignKey(
        "challenges.Moathon",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "moathon"],
                name="unique_like_per_user_moathon",
            )
        ]
        indexes = [
            models.Index(fields=["moathon", "created_at"]),
            models.Index(fields=["user", "created_at"]),
        ]