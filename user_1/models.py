from django.db import models

# Create your models here. 

class Property_detail(models.Model): 
    property_id=models.IntegerField(primary_key=True)
    property_type=models.CharField(max_length=150) 
    property_age=models.IntegerField()
    selling_option=models.CharField(max_length=150) 
    construction_status=models.CharField(max_length=150) 
    floor=models.IntegerField()
    bhk=models.IntegerField()
    bathroom=models.IntegerField()
    balcony=models.IntegerField()
    furnish_type=models.CharField(max_length=150)
    geography_area=models.CharField(max_length=150)
    parking_type=models.CharField(max_length=150)
    property_value=models.CharField(max_length=150)
    property_rent_price=models.CharField(max_length=150)
    from_avail_property_date=models.DateField()
    property_address=models.CharField(max_length=150)

    def __str__(self) -> str:
        return super().__str__()

class Property_other_detail(models.Model): 
    # Property media like image and video or many other detail will be here.
    media_id=models.ForeignKey(Property_detail, on_delete=models.CASCADE) 
    property_image_1=models.FileField(upload_to="media/") 
    property_image_2=models.FileField(upload_to="media/") 
    property_image_3=models.FileField(upload_to="media/") 
