import uuid
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class p_detail_v1(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property_data = models.JSONField()
    property_other_data = models.JSONField(default=dict)

    def __str__(self):
        return self.name

class property_utility_v1(models.Model):
    property_id = models.ForeignKey(p_detail_v1, on_delete=models.CASCADE)
    seller_id = models.CharField(max_length=200)
    property_report = models.JSONField(default=dict)

    
class User_other_utils(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_mobile = models.CharField(max_length=200, null=True)
    user_other_data_json = models.JSONField(default=dict)

    def __str__(self):
        return self.name