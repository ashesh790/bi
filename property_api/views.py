from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from user_1.models import p_detail_v1, property_utility_v1
from .serializers import property_serializer, property_with_utils
from django.contrib.auth.models import User
from rest_framework.decorators import api_view 
from rest_framework.response import Response

class PropertyListAPIView(generics.ListAPIView):
    queryset = p_detail_v1.objects.all()
    serializer_class = property_serializer

@api_view(['GET']) 
def all_property_data(request): 
    property_query = p_detail_v1.objects.all() 
    property_serializer_data = property_with_utils(many = True)
    serializer_data = property_serializer_data.data 

    response_data = {
        "property_data" : serializer_data
    }

    return Response(response_data)