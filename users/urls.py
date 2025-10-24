# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
]