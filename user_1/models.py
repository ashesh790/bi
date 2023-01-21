from django.db import models

# Create your models here. 

class main_seller_info(models.Model): 
    order_id=models.IntegerField(primary_key=True, auto_created=True) 
    seller_id=models.CharField(max_length=11) 
    property_title=models.CharField(max_length=100) 
    selling_option=models.TextField() 
    property_desc=models.TextField()
    property_images=models.TextField()   
    property_video=models.TextField()   
    property_current_status=models.TextField() 
    property_location=models.TextField() 
    property_other_info=models.TextField() 
    update_time_stamp=models.TextField() 
    # sample_image=models.ImageField(upload_to='media', null=True)  
    