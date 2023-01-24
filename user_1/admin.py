from django.contrib import admin

from user_1.models import Property_detail, Property_other_detail

# Register your models here.
# class main_seller_infoAdmin(admin.ModelAdmin): 
#     list_display = ("order_id",
#                     "seller_id",
#                     "property_title",
#                     "selling_option",
#                     "property_desc",
#                     "property_media",
#                     "property_current_status",
#                     "property_location",
#                     "property_other_info",
#                     "update_time_stamp",
#                     )
admin.site.register(Property_detail) 
admin.site.register(Property_other_detail)