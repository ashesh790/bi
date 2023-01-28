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
    path('add_property_image', views.add_property_image, name="add-property-image"), 
    path('show_property_detail/<int:property_id>/', views.show_property_detail, name="show-property-detail"), 
    path('delete_property_record/<int:property_id>/', views.delete_property, name="delete-property-record"), 
    path('update_property_record/<int:property_id>/',views.update_property, name="update-property")  
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
