from django.urls import path
from .views import PropertyListAPIView
from property_api import views

urlpatterns = [
    path('properties/', PropertyListAPIView.as_view(), name='property-list'),
]
