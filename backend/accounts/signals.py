from django.db.models.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import User, UserBadge, Badge
from .badge_functions import award_badges_to_user  # 뱃지 처리 함수

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    """
    유저가 로그인할 때마다 뱃지 조건을 점검하고 적합한 뱃지를 추가합니다.
    """
    # 로그인한 유저에 대해 뱃지 업데이트
    award_badges_to_user(user)