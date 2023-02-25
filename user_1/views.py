import json
import os
import uuid
from django.core.files.storage import default_storage
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from staying_source.settings import MEDIA_ROOT, MEDIA_URL
from user_1.apis.fetch_api.main_functions import add_property_details_in_database, delete_all_property_data, get_all_property_data, update_property_data_record, upload_property_image
from user_1.apis.fetch_api.state_management.handle_state import login_user, signup_user
from user_1.models import User_register, p_detail 
from django.core.serializers import serialize 
import shutil 
from django.core.files.storage import FileSystemStorage

# from user_1.forms import MyForm

# Note: Create login and signup in single html page 

# Login function 
def sign_up(request): 
    if request.method =="POST": 
        user_name=request.POST['user_name'] 
        user_email=request.POST['user_email'] 
        user_mobile=request.POST['user_number'] 
        user_psw=request.POST['user_psw'] 

        if User_register.objects.filter(user_name=user_name): 
            print("Existing User!") 
            return redirect("login") 
        if User_register.objects.filter(user_email=user_email).exists():
            print("Email is already exist!") 
            return redirect("login") 
        if len(user_name)>20: 
            print("USer must be under 20 character") 
            return redirect("login") 
        if not user_name.isalnum(): 
            print("User name must be alphanumeric") 
            return redirect("login") 
        
        new_user=User_register.objects.create(user_name=user_name, user_email=user_email, user_mobile=user_mobile,user_psw=user_psw) 
        if new_user: 
            return redirect('login') 
        else: 
            return False 
    else: 
        return render(request, "theme/signup.html")

# sign up
def login(request): 
    if request.POST: 
        login_user(request)  
        return render(request, 'theme/index.html')
    return render(request, "theme/login.html") 
     
# logout 
def logout(request): 
    if request: 
        try: 
            del request.session['user_name'] 
        except: 
            print("Logout") 
    return render(request, 'theme/login.html') 

def dashboard(request): 
    data=p_detail.objects.filter(seller_id=User_register.objects.get(user_id=request.session._session['user_id']))
    return render(request, 'admin/admin2/dashboard.html', {'data':data})
def crud_property(request): 
    data=p_detail.objects.filter(seller_id=User_register.objects.get(user_id=request.session._session['user_id']))  
    return render(request, 'record.html', {'data':data}) 
# Render home page 

def home(request):
    return render(request, 'theme/index.html') 
def home1(request): 
    # try:
    other_data=p_detail.objects.all()
    list_object=[]
    for i in other_data: 
        list_object.append(i) 
    # list_object=json.dumps(str(list_object[0].property_data).replace('_', ' '))
    return render(request, 'index.html', {'data':list_object})  

def about_us(request): 
    return render(request, 'theme/about.html') 

def contact(request): 
    return render(request, 'theme/contact.html')

def property_agent(request): 
    return render(request, 'theme/property-agent.html')

def property_type(request): 
    return render(request, 'theme/property-type.html')

def property_list(request): 
    return render(request, 'theme/property-list.html') 
def add_property_details(request):    
    try:
        if request.method =='POST' and len(request.POST) is not None: 
            property_details=add_property_details_in_database(request) 
            return render(request, 'admin/admin2/add_property.html')   
        return render(request, 'admin/admin2/add_property.html')  
    except Exception as ex: 
        print(f"Solve this: {ex}") 
    return render(request, 'admin/admin2/add_property.html') 


def show_property_detail(request,property_id):
    try: 
        property_id=property_id  
        data=get_all_property_data(property_id=property_id)   
        template=loader.get_template('show_property_detail.html')
        context={
            "data":data, 
        }
        return HttpResponse(template.render(context, request)) 
    except Exception as ex: 
        print(f"Solve this: {ex}") 


def delete_property(request, property_id): 
    try: 
        property_id=property_id  
        delete_all_property_data(property_id)  
        # template=loader.get_template('property_basic_detail.html') 
        context={}
        return render(request,'property_basic_detail.html') 
    except Exception as ex: 
        print(f"Solve this: {ex}") 
    return render(request,'property_basic_detail.html')

def update_property(request, property_id=0): 
    # postData = request.get_json()
    try: 
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if request.method == 'POST': 
            data=p_detail.objects.get(id=property_id)
            property_id=property_id
            data.property_data['property_type'] = request.POST['data[property_type]']  
            data.property_data['property_age'] = request.POST['data[property_age]']  
            data.property_data['selling_option'] = request.POST['data[selling_option]']  
            data.property_data['construction_status'] = request.POST['data[construction_status]']  
            data.property_data['floor'] = request.POST['data[floor]']  
            data.property_data['bathroom'] = request.POST['data[bathroom]']  
            data.property_data['balcony'] = request.POST['data[balcony]']  
            data.property_data['bhk'] = request.POST['data[bhk]']  
            data.property_data['furnish_type'] = request.POST['data[furnish_type]']  
            data.property_data['geography_area'] = request.POST['data[geography_area]']  
            data.property_data['parking_type'] = request.POST['data[parking_type]']  
            data.property_data['property_value'] = request.POST['data[property_value]']  
            data.property_data['property_rent_price'] = request.POST['data[property_rent_price]']  
            data.property_data['from_avail_property_date'] = request.POST['data[from_avail_property_date]']  
            data.property_data['property_address'] = request.POST['data[property_address]'] 
                      
            data.save()  
            return render(request, 'update_property_data.html', {'data':data, "id":property_id})
        property_id=property_id
        data=p_detail.objects.get(id=property_id) 
        property_data=data.property_data
        return render(request, 'update_property_data.html', {'data':property_data, "id":property_id})
    except Exception as ex: 
        print(f"Solve this: {ex}") 
    return render(request, 'update_property_data.html', {'data':property_data, "id":property_id})  

def manage_image_upload(request,property_id): 
    upload_property_image(request, property_id) 
    return render(request, "image.html", {'id':property_id})  
def property_status(request): 
    pass

def test_html_page(request): 
    return render(request, 'test.html') 

