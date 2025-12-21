from django.urls import path
from . import views

urlpatterns = [
    path('find_password/', views.find_password),
    path('reset_password/', views.reset_password),
    path('profile/', views.profile),
    path("profile/update/", views.profile_update),
    path("onboarding/", views.onboarding),
]