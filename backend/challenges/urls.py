from django.urls import path
from . import views

urlpatterns = [
    path('', views.moathon_list),
    path('<int:moathon_pk>/', views.moathon_detail),
]