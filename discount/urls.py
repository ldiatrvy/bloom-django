from django.urls import path
from . import views
urlpatterns = [
    path('',views.discount_home, name='discount_home'),
    path('<int:pk>',views.DiscountDetailView.as_view(),name='discount-detail'),
]