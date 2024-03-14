import uuid
from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class p_detail_v1(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    property_data = models.JSONField()
    property_other_data = models.JSONField(default=dict)    

    # def __str__(self):
        # return self.seller_id
    
class User_other_utils(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_mobile = models.CharField(max_length=200, null=True)
    user_other_data_json = models.JSONField(default=dict)
    is_brocker = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        # Extracting mobile key from JSON field and storing it in user_mobile column
        if 'user_mobile' in self.user_other_data_json:
            self.user_mobile = self.user_other_data_json['user_mobile']
            del self.user_other_data_json['mobile']
        super().save(*args, **kwargs)
    # def __str__(self):
        # return self.user_id