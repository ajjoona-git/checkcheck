from django.urls import path
from . import views

urlpatterns = [
    path('recommend_product/', views.recommend_product),   # 금융 상품 추천 API
]