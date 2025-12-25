from __future__ import annotations

from datetime import date
from typing import Optional

from django.db import IntegrityError, transaction

from accounts.models import Badge, UserBadge, UserFollow
from challenges.models import Moathon, MoathonComment, MoathonLike

# track
TRACK_25 = "첫 번째 숨 고르기"
TRACK_50 = "반환점 터치"
TRACK_75 = "막판 스퍼트!"
TRACK_100 = "완주 트로피"

# achieve
ACH_START = "시작이 반"
ACH_DEPOSIT = "티끌 모아 태산"
ACH_3DAYS = "작심삼일 탈출"
ACH_PRO = "프로 완주러"
ACH_BILLIONAIRE = "억만장자의 꿈"

# social
SOC_CHEERLEADER = "응원 단장"
SOC_COMMENTS = "소통 요정"
SOC_BELOVED = "인기 스타"
SOC_FOLLOWERS = "팔로팔로미"

def award_all_badges(user) -> None:
    with transaction.atomic():
        award_track_badges(user)
        award_achieve_badges(user)
        award_social_badges(user)

# 회원가입 직후
def award_signup_badges(user) -> None:
    with transaction.atomic():
        _grant(user, "achieve", ACH_START)

# 모아톤 생성 직후(티끌 모아 태산, 억만장자의 꿈)
def award_achieve_badges_on_moathon_created(user, moathon: Moathon) -> None:
    with transaction.atomic():
        _grant(user, "achieve", ACH_DEPOSIT)

        term_months = _get_term_months_by_save_trm(moathon)
        if term_months is not None and term_months >= 36:
            _grant(user, "achieve", ACH_BILLIONAIRE)

# 모아톤 진행률 기반 트랙 뱃지 지급
def award_track_badges(user) -> None:
    today = date.today()
    moathons = Moathon.objects.filter(user=user).only("id", "start_date", "end_date")

    for m in moathons:
        progress = _progress_rate(m, today=today)

        # 누적 지급 방식
        if progress >= 25:
            _grant_track(user, "track", TRACK_25, moathon=m)
        if progress >= 50:
            _grant_track(user, "track", TRACK_50, moathon=m)
        if progress >= 75:
            _grant_track(user, "track", TRACK_75, moathon=m)
        if progress >= 100:
            _grant_track(user, "track", TRACK_100, moathon=m)

# 달성일수 기반 뱃지 지급
def award_achieve_badges(user) -> None:
    today = date.today()
    moathons = Moathon.objects.filter(user=user).only("id", "start_date", "end_date")

    # 작심삼일 탈출(모아톤별)
    for m in moathons:
        if _maintained_days(m, today=today) >= 3:
            _grant(user, "achieve", ACH_3DAYS)

    # 프로 완주러(유저당 1회)
    expired_cnt = Moathon.objects.filter(user=user, end_date__lt=today).count()
    if expired_cnt >= 3:
        _grant(user, "achieve", ACH_PRO)

# 소셜 뱃지 지급
def award_social_badges(user) -> None:
    # 소통요정: 내가 작성한 댓글 5개 이상
    my_comment_cnt = MoathonComment.objects.filter(user=user).count()
    if my_comment_cnt >= 5:
        _grant(user, "social", SOC_COMMENTS)

    # 응원단장: 내가 타인 모아톤에 누른 좋아요 10회
    cheer_cnt = MoathonLike.objects.filter(user=user).exclude(moathon__user=user).count()
    if cheer_cnt >= 10:
        _grant(user, "social", SOC_CHEERLEADER)

    # 인기스타: 내 모아톤이 받은 좋아요 20개
    beloved_cnt = MoathonLike.objects.filter(moathon__user=user).exclude(user=user).count()
    if beloved_cnt >= 20:
        _grant(user, "social", SOC_BELOVED)

    # 팔로팔로미: 팔로워 10명
    follower_cnt = UserFollow.objects.filter(following=user).count()
    if follower_cnt >= 10:
        _grant(user, "social", SOC_FOLLOWERS)

# 모아톤 진행률 계산
def _progress_rate(moathon: Moathon, today: date) -> int:
    total_days = (moathon.end_date - moathon.start_date).days
    elapsed_days = (today - moathon.start_date).days
    if total_days <= 0:
        return 100
    if elapsed_days <= 0:
        return 0
    return min(int((elapsed_days / total_days) * 100), 100)

# 모아톤 유지 일수 계산
def _maintained_days(moathon: Moathon, today: date) -> int:
    effective_end = min(today, moathon.end_date)
    return (effective_end - moathon.start_date).days

# 만기 36개월 이상 판단
def _get_term_months_by_save_trm(moathon: Moathon) -> Optional[int]:
    trm = getattr(getattr(moathon, "product_option", None), "save_trm", None)
    if trm is None:
        return None

    trm_str = str(trm).strip()
    if not trm_str:
        return None

    try:
        return int(trm_str)
    except (TypeError, ValueError):
        return None

# 뱃지 객체 조회
def _get_badge(badge_type: str, badge_name: str) -> Optional[Badge]:
    try:
        return Badge.objects.get(type=badge_type, name=badge_name)
    except Badge.DoesNotExist:
        return None

# 트랙 뱃지 지급
def _grant_track(user, badge_type: str, badge_name: str, moathon=None) -> None:
    badge = _get_badge(badge_type, badge_name)
    if not badge:
        return

    try:
        UserBadge.objects.get_or_create(user=user, badge=badge, moathon=moathon)
    except IntegrityError:
        pass

# 일반 뱃지 지급
def _grant(user, badge_type: str, badge_name: str) -> None:
    badge = _get_badge(badge_type, badge_name)
    if not badge:
        return

    try:
        UserBadge.objects.get_or_create(user=user, badge=badge)
    except IntegrityError:
        pass