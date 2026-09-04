from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.medicine_search, name='medicine_search'),
    path('scan-prescription/', views.scan_prescription, name='scan_prescription'),
]