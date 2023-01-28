from django.contrib import admin

from user_1.models import Property_detail, Property_other_detail, User_register

class User_register_admin(admin.ModelAdmin): 
    list_display=[
        'user_name','user_email','user_mobile','user_gender','user_psw' 
    ]
class Property_detail_admin(admin.ModelAdmin): 
    list_display=[
        'seller_id', 
        'property_id',
        'property_type',
        'property_age',
        'selling_option',
        'construction_status',
        'floor',
        'bhk',
        'bathroom',
        'balcony',
        'furnish_type',
        'geography_area',
        'parking_type',
        'property_value',
        'property_rent_price',
        'from_avail_property_date',
        'property_address', 
    ] 

class Property_other_detail_admin(admin.ModelAdmin): 
    list_display=[
        'media_id', 'property_image_1','property_image_2','property_image_3'
    ]
    model=Property_other_detail 

class Brand_admin(admin.ModelAdmin): 
    model=Property_detail
    inlines=[
        Property_other_detail_admin 
    ]

# Register your models here.
admin.site.register(Property_detail, Property_detail_admin) 
admin.site.register(Property_other_detail, Property_other_detail_admin) 
admin.site.register(User_register, User_register_admin) 