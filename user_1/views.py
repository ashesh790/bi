import json
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from django.contrib import messages
from user_1.apis.fetch_api.main_functions import add_property_details_in_database, delete_all_property_data, get_all_property_data, update_property_data_record
from user_1.models import Property_detail 
from django.core.serializers import serialize 
# from user_1.forms import MyForm

# Note: Create login and signup in single html page 

# Login function 
def login(request): 
    return render(request, 'login.html')

# sign up
def sign_up(request): 
    pass 

# logout 
def logout(request): 
    pass 

# Render home page 
def home(request): 
    data="Hello world"
    return render(request, 'index.html', {'data':data})   

def add_property_details(request):    
    if request.method =='POST' and len(request.POST) is not None: 
        add_property_details_in_database(request) 
    else: 
        print("Please Fill tha all necessary fields")  
    return render(request, 'property_basic_detail.html') 

def show_property_detail(request,property_id):
    property_id=property_id  
    data=get_all_property_data(property_id=property_id)   
    template=loader.get_template('show_property_detail.html')
    context={
        "data":data, 
    }
    return HttpResponse(template.render(context, request))

def delete_property(request, property_id):
    property_id=property_id  
    delete_all_property_data(property_id)  
    # template=loader.get_template('property_basic_detail.html') 
    context={}
    return render(request,'property_basic_detail.html') 

def update_property(request, property_id): 
    property_id=property_id
    update=update_property_data_record(property_id) 
    return render(request, 'property_basic_detail.html')  
def property_status(request): 
    pass 