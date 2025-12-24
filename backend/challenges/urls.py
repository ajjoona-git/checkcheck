from django.urls import path
from . import views

urlpatterns = [
    path('', views.moathon_list),
    path('create/', views.moathon_create),
    path('following/', views.following_moathon_list),

    path('<int:moathon_pk>/', views.moathon_detail),
    path("<int:moathon_pk>/comments/", views.moathon_comment_list_create),
    path("<int:moathon_pk>/comments/<int:comment_pk>/", views.moathon_comment_detail),
    path("<int:moathon_pk>/like/", views.moathon_like_toggle),
]
