from django import forms 
from .models import main_seller_info 
# Create your models here.
class MyForm(forms.Form):
    property_title=forms.CharField()  
    selling_option=forms.CharField() 
    property_desc=forms.CharField()
    property_images_1=forms.FileField()
    property_images_2=forms.FileField()
    property_images_3=forms.FileField()
    property_video=forms.FileField() 
    property_current_status=forms.CharField() 
    property_location=forms.CharField() 
    property_other_info=forms.CharField() 
    update_time_stamp=forms.CharField()