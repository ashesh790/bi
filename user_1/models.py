import uuid
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class User_register(models.Model):
    user_id = models.SlugField(
        primary_key=True, unique=True, auto_created=True, default=uuid.uuid1
    )
    user_name = models.CharField(max_length=200)
    user_email = models.CharField(max_length=200)
    user_mobile = models.CharField(max_length=200, null=True)
    user_gender = models.CharField(max_length=200)
    user_psw = models.CharField(max_length=200)
    user_other_data = models.JSONField(default=dict)


# Using right now
class p_detail(models.Model):
    seller_id = models.ForeignKey(User_register, on_delete=models.CASCADE)
    property_data = models.JSONField()
    property_other_data = models.JSONField(default=dict)


class property_utility(models.Model):
    property_id = models.ForeignKey(p_detail, on_delete=models.CASCADE)
    seller_id = models.CharField(max_length=200)
    property_report = models.JSONField(default=dict) 

class p_detail_v1(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property_data = models.JSONField()
    property_other_data = models.JSONField(default=dict)


class property_utility_v1(models.Model):
    property_id = models.ForeignKey(p_detail_v1, on_delete=models.CASCADE)
    seller_id = models.CharField(max_length=200)
    property_report = models.JSONField(default=dict)


class User_other_utils(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_mobile = models.CharField(max_length=200, null=True)
    user_other_data_json = models.JSONField(default=dict)