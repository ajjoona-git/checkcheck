from django.urls import path
from . import views

urlpatterns = [
    path('find_password/', views.find_password),
    path('reset_password/', views.reset_password),
]