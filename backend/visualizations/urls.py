from django.urls import path
from . import views

urlpatterns = [
    path("commodities/prices/", views.commodity_price_series),
]