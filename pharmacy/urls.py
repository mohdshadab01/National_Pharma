from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),
]