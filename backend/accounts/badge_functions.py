from django.db import transaction
from .models import UserBadge, Badge
from datetime import date

def award_badges_to_user(user):
    """
    유저가 로그인할 때마다 뱃지 조건을 점검하고 적합한 뱃지를 추가합니다.
    """
    # 트랜잭션을 사용하여 중복 삽입 방지
    with transaction.atomic():
        # 1. 트랙 뱃지 체크
        for moathon in user.moathons.all():
            check_track_badges(user, moathon)

        # 2. 어치브 뱃지 체크
        check_achieve_badges(user)

        # 3. 소셜 뱃지 체크
        check_social_badges(user)

def check_track_badges(user, moathon):
    """
    진행률에 따라 트랙 뱃지 추가
    """
    # 진행률 계산 (serializer에서의 진행률 계산 로직을 그대로 사용)
    total_days = (moathon.end_date - moathon.start_date).days
    elapsed_days = (date.today() - moathon.start_date).days

    if total_days <= 0:
        progress_rate = 100
    elif elapsed_days <= 0:
        progress_rate = 0
    else:
        progress_rate = min((elapsed_days / total_days) * 100, 100)

    badges_to_award = []

    # 진행률에 맞는 뱃지 추가
    if 0.25 <= progress_rate < 0.5:
        badges_to_award.append('badge_track_25')
    if 0.5 <= progress_rate < 0.75:
        badges_to_award.append('badge_track_50')
    if 0.75 <= progress_rate < 1.0:
        badges_to_award.append('badge_track_75')
    if progress_rate == 100:
        badges_to_award.append('badge_track_100')

    # UserBadge에 추가
    for badge_name in badges_to_award:
        try:
            badge = Badge.objects.get(name=badge_name, type='track')
            UserBadge.objects.get_or_create(user=user, badge=badge, moathon=moathon)
        except Badge.DoesNotExist:
            pass  # 뱃지가 존재하지 않으면 그냥 무시

def check_achieve_badges(user):
    """
    어치브 뱃지 조건 체크
    """
    # 예시: 저축 금액이 1000만 원 이상이면 뱃지 추가
    if user.total_savings >= 10000000:
        try:
            badge = Badge.objects.get(name='badge_achieve_billionaire', type='achieve')
            UserBadge.objects.get_or_create(user=user, badge=badge)
        except Badge.DoesNotExist:
            pass  # 뱃지가 존재하지 않으면 그냥 무시

    # 예시: 3개의 모아톤을 성공한 경우
    if user.moathons.count() >= 3:
        try:
            badge = Badge.objects.get(name='badge_achieve_3moathons', type='achieve')
            UserBadge.objects.get_or_create(user=user, badge=badge)
        except Badge.DoesNotExist:
            pass  # 뱃지가 존재하지 않으면 그냥 무시

def check_social_badges(user):
    """
    소셜 뱃지 조건 체크
    """
    # 예시: 팔로워가 10명을 넘으면 뱃지 추가
    if user.likes_received >= 10:
        try:
            badge = Badge.objects.get(name='badge_social_followers', type='social')
            UserBadge.objects.get_or_create(user=user, badge=badge)
        except Badge.DoesNotExist:
            pass  # 뱃지가 존재하지 않으면 그냥 무시

    # 예시: 20개의 좋아요를 받은 경우
    if user.comments_received >= 20:
        try:
            badge = Badge.objects.get(name='badge_social_beloved', type='social')
            UserBadge.objects.get_or_create(user=user, badge=badge)
        except Badge.DoesNotExist:
            pass  # 뱃지가 존재하지 않으면 그냥 무시
