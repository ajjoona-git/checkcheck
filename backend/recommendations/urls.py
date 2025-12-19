from django.urls import path
from . import views

urlpatterns = [
    path('recommend_product/', views.recommend_product),
]