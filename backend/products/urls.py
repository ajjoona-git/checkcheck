from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list),                       # 전체 금융 상품 조회
    path('<int:product_id>/', views.product_detail),    # 금융 상품 상세 조회
    path('banklist/', views.bank_list),                 # 은행 목록 조회
]
