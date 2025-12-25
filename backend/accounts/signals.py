from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from accounts.services.badge_functions import award_all_badges, award_signup_badges

User = get_user_model()

# 회원가입 직후 뱃지 지급
@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    if kwargs.get("raw", False):
        return
    if created:
        award_signup_badges(instance)

# 로그인 직후 뱃지 점검 및 지급
@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    award_all_badges(user)