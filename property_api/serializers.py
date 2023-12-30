from rest_framework import serializers
from user_1.models import p_detail_v1

class property_serializer(serializers.ModelSerializer):
    class Meta:
        model = p_detail_v1
        fields = '__all__'
