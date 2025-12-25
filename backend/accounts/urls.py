from django.urls import path
from . import views

urlpatterns = [
    path('find_password/', views.find_password),    # 비밀번호 찾기(이메일 인증)
    path('reset_password/', views.reset_password),  # 비밀번호 재설정
    path('profile/', views.profile),                # 사용자 프로필 조회
    path("profile/update/", views.profile_update),  # 사용자 프로필 수정
    path("onboarding/", views.onboarding),          # 온보딩 정보 제출
    path('badge_collection', views.badge_collection),   # 뱃지 도감 조회
    path("<int:user_pk>/follow/", views.follow_toggle), # 팔로우/언팔로우 토글
]