from rest_framework import serializers
from user_1.models import p_detail_v1, property_utility_v1

class property_serializer(serializers.ModelSerializer):
    class Meta:
        model = p_detail_v1
        fields = '__all__'

class property_utility(serializers.ModelSerializer): 
    class Meta: 
        model = property_utility_v1 
        fields = '__all__'

class property_with_utils(serializers.ModelSerializer): 
    property_query = property_serializer() 
    class Meta:
        model = property_utility_v1 
        fields = '__all__'
