from django.contrib import admin

from user_1.models import User_register, p_detail, property_utility


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


# Register your models here.

admin.site.register(User_register, User_register_admin)
admin.site.register(p_detail, p_detail_admin)
admin.site.register(property_utility, property_utility_admin)
