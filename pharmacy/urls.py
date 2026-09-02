from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('medicine-search/', views.medicine_search, name='medicine_search'),
    path('upload-prescription/', views.upload_prescription, name='upload_prescription'),
    path('cart/', views.cart, name='cart'),
    path('microbiology/', views.microbiology, name='microbiology'),
    path('contact/', views.contact, name='contact'),
]