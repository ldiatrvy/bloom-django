from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
]