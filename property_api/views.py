from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from user_1.models import p_detail_v1
from .serializers import property_serializer 
from django.contrib.auth.models import User
from rest_framework.decorators import api_view 
from rest_framework.response import Response

class PropertyListAPIView(generics.ListAPIView):
    queryset = p_detail_v1.objects.all()
    serializer_class = property_serializer
