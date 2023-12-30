from django.urls import path
from .views import Property_create_api_view, PropertyListAPIView
from property_api import views

urlpatterns = [
    path('properties/', PropertyListAPIView.as_view(), name='property-list'),
    path('add_properties/', Property_create_api_view.as_view(), name='property-create'),
]
