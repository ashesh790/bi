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
    path("", views.home, name="test_html_page"), 
    path('home', views.home, name="home"), 
    path('signup',views.sign_up, name="signup"),  
    path('login',views.login, name="login"),  
    path('logout',views.logout, name="logout"),  
    path('add_property_details',views.add_property_details, name="add_property_details"), 
    path('show_property_detail/<int:property_id>/', views.show_property_detail, name="show-property-detail"), 
    path('delete_property_record/<int:property_id>/', views.delete_property, name="delete-property-record"), 
    path('update_property_record/<int:property_id>/delete_property_image/<str:image_name>/', views.delete_property_image, name="delete_property_record"), 
    path('update_property_record/<int:property_id>/',views.update_property, name="update-property"), 
    path("crud_property", views.crud_property, name="crud_property"), 
    path("images/<int:property_id>/", views.manage_image_upload, name="manage_image_upload"), 
    path("dashboard", views.dashboard, name="dashboard"), 
    path("about", views.about_us, name="about"), 
    path("contact", views.contact, name="contact"), 
    path("property_agent", views.property_agent, name="property_agent"), 
    path("property_type", views.print_property_type, name="property_type"), 
    path("property_list", views.property_list, name="property_list"), 
    path("property_category_wise/<str:property_type>/", views.property_category_wise, name="property_category_wise"), 
    path("property_sell_option_wise", views.property_sell_option_wise, name="property_sell_option_wise"), 
    path("property_details/<int:property_id>/", views.show_full_property_detail, name="property_details"), 
    path("show_required_model", views.property_post_modal_management, name="property_post_modal_management"), 
    path("test_function", views.test_function, name="test_function"), 
    path("inquiries_from_user", views.inquiries_from_user, name="inquiries_from_user"), 
    path("prop_table", views.prop_table, name="prop_table"), 
    path("property_type_list", views.property_type_list, name="property_type_list"), 
    path("advance_filter", views.advance_filter, name="advance_filter"), 
    path("advance_filter_boundary", views.advance_filter_boundary, name="advance_filter_boundary"), 
    path("country_list", views.country_list, name="country_list"), 
    path("state_list", views.state_list, name="state_list"),
    path("city_list", views.city_list, name="city_list"), 
    path("search_properties", views.search_properties, name="search_properties"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
