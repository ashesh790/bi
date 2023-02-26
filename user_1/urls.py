"""staying_source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user_1 import views 
urlpatterns = [
    path('home', views.home, name="home"), 
    path('signup',views.sign_up, name="signup"),  
    path('login',views.login, name="login"),  
    path('logout',views.logout, name="login"),  
    path('add_property_details',views.add_property_details, name="add_property_details"), 
    path('show_property_detail/<int:property_id>/', views.show_property_detail, name="show-property-detail"), 
    path('delete_property_record/<int:property_id>/', views.delete_property, name="delete-property-record"), 
    path('update_property_record/<int:property_id>/delete_property_image/<str:image_name>/', views.delete_property_image, name="delete-property-image"), 
    path('update_property_record/<int:property_id>/',views.update_property, name="update-property"), 
    path("", views.test_html_page, name="test_html_page"), 
    path("crud_property", views.crud_property, name="crud_property"), 
    path("images/<int:property_id>/", views.manage_image_upload, name="manage_image_upload"), 
    path("dashboard", views.dashboard, name="dashboard"), 
    path("about", views.about_us, name="about_us"), 
    path("contact", views.contact, name="contact"), 
    path("property_agent", views.property_agent, name="property_agent"), 
    path("property_type", views.property_type, name="property_type"), 
    path("property_list", views.property_list, name="property_list"), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
