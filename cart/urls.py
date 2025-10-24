from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:bouquet_id>/', views.cart_add, name='cart_add'),
    path('update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('remove/<int:bouquet_id>/', views.cart_remove, name='cart_remove'),
    path('decrease/<int:bouquet_id>/', views.cart_decrease, name='cart_decrease'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('apply-discount/', views.apply_discount, name='apply_discount'),
]