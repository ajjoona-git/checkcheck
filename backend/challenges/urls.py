from django.urls import path
from . import views

urlpatterns = [
    path('', views.moathon_list),                       # 전체 모아톤 조회
    path('create/', views.moathon_create),              # 모아톤 생성
    path('following/', views.following_moathon_list),   # 팔로우 중인 유저 모아톤 조회

    path('<int:moathon_pk>/', views.moathon_detail),                            # 모아톤 상세/수정/삭제
    path("<int:moathon_pk>/comments/", views.moathon_comment_list_create),      # 모아톤 댓글 목록 조회/작성
    path("<int:moathon_pk>/comments/<int:comment_pk>/", views.moathon_comment_detail),  # 모아톤 댓글 수정/삭제
    path("<int:moathon_pk>/like/", views.moathon_like_toggle),                  # 모아톤 좋아요/취소 
]
