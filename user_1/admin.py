from django.contrib import admin

from user_1.models import Property_detail, Property_other_detail, User_register, p_detail

class User_register_admin(admin.ModelAdmin): 
    list_display=[
        'user_name','user_email','user_mobile','user_gender','user_psw' 
    ]
class p_detail_admin(admin.ModelAdmin): 
    list_display=[
        'id','seller_id','property_data' 
    ]

# Register your models here.

admin.site.register(User_register, User_register_admin) 
admin.site.register(p_detail, p_detail_admin) 