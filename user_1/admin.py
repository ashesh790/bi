from django.contrib import admin

from user_1.models import User_other_utils, User_register, p_detail, p_detail_v1, property_utility, property_utility_v1


class User_register_admin(admin.ModelAdmin):
    list_display = [
        "user_id",
        "user_name",
        "user_email",
        "user_mobile",
        "user_gender",
        "user_psw",
        "user_other_data",
    ]


class p_detail_admin(admin.ModelAdmin):
    list_display = ["id", "seller_id", "property_data", "property_other_data"]


class property_utility_admin(admin.ModelAdmin):
    list_display = ["id", "property_id", "seller_id", "property_report"]

class property_utility_v1_admin(admin.ModelAdmin): 
    list_display = ["id", "property_id", "seller_id", "property_report"]

class p_detail_v1_admin(admin.ModelAdmin): 
    list_display = ["id", "seller_id", "property_data", "property_other_data"]

class User_other_utils_admin(admin.ModelAdmin): 
    list_display = ["user_id", "user_mobile", "user_other_data_json"]
# Register your models here.

admin.site.register(User_register, User_register_admin)
admin.site.register(p_detail, p_detail_admin)
admin.site.register(property_utility, property_utility_admin)
admin.site.register(p_detail_v1, p_detail_v1_admin)
admin.site.register(property_utility_v1, property_utility_v1_admin) 
admin.site.register(User_other_utils, User_other_utils_admin)
