import uuid
from django.db import models

# Create your models here.


class User_register(models.Model):
    user_id = models.SlugField(
        primary_key=True, unique=True, auto_created=True, default=uuid.uuid1
    )
    user_name = models.CharField(max_length=20)
    user_email = models.CharField(max_length=25)
    user_mobile = models.CharField(max_length=20, null=True)
    user_gender = models.CharField(max_length=5)
    user_psw = models.CharField(max_length=10)
    user_other_data = models.JSONField(default=dict)


# Using right now
class p_detail(models.Model):
    seller_id = models.ForeignKey(User_register, on_delete=models.CASCADE)
    property_data = models.JSONField()
    property_other_data = models.JSONField(default=dict) 