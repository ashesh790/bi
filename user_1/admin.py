from django.contrib import admin

from user_1.models import main_seller_info

# Register your models here.
class main_seller_infoAdmin(admin.ModelAdmin): 
    list_display = ("order_id",
                    "seller_id",
                    "property_title",
                    "selling_option",
                    "property_desc",
                    "property_media",
                    "property_current_status",
                    "property_location",
                    "property_other_info",
                    "update_time_stamp",
                    )
admin.site.register(main_seller_info, main_seller_infoAdmin)