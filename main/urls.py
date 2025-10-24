from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='catalog_flow'),
    path('description/<int:bouquet_id>/',views.description, name='description'),
]