from django.urls import path
from . import views

urlpatterns = [
    path("commodities/prices/", views.commodity_price_series),  # 원자재 가격 시계열 데이터 조회 API
]