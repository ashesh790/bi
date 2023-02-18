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
from user_1.apis.fetch_api.main_functions import add_property_details_in_database, delete_all_property_data, get_all_property_data, update_property_data_record
from user_1.apis.fetch_api.state_management.handle_state import login_user, signup_user
from user_1.models import User_register, p_detail 
from django.core.serializers import serialize 
import shutil 
from django.core.files.storage import FileSystemStorage

# from user_1.forms import MyForm

# Note: Create login and signup in single html page 

# Login function 
def sign_up(request): 
    try: 
        signup_user(request) 
        return render(request, 'sign_up.html') 
    except Exception as ex: 
        print(f"Solve this: {ex}") 


# sign up
def login(request): 
    try: 
        if request.POST: 
            login_user(request)  
            return redirect("home")
        return render(request, "theme/login.html") 
    except Exception as ex: 
        print(f"Solve this: {ex}") 
    return render(request, "theme/login.html") 


# logout 
def logout(request): 
    if request: 
        try: 
            del request.session['user_name'] 
        except: 
            print("Logout") 
    return render(request, 'login.html') 

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
            return render(request, 'property_basic_detail.html')   
        else: 
            print("Please Fill tha all necessary fields")  
        return render(request, 'property_basic_detail.html')  
    except Exception as ex: 
        print(f"Solve this: {ex}") 
    return render(request, 'property_basic_detail.html') 


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
            # if request.method =="FILES": 
            #     data.property_data['property_image_1'],property_image_1 = request.FILES['property_image_1']
            #     data.property_data['property_image_2'],property_image_2 = request.FILES['property_image_2']
            #     data.property_data['property_image_3'],property_image_3 = request.FILES['property_image_3']

            #     property_media=[property_image_1, property_image_2, property_image_3] 
            #     property_media_save=[] 
            #     fss = FileSystemStorage() 
            #     for i in property_media: 
            #         file = fss.save(i.name, i)
            #         file_url = fss.url(file)
            #         property_media_save.append(file_url) 
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
    user_id=request.session['user_id'] 
    data=p_detail.objects.get(id=property_id)  
    if request.method =="POST": 
        data.property_data['property_value'] = "909090909"  
        images=request.FILES.getlist('images')
        data.save()
        property_media_save=[] 
        fss = FileSystemStorage() 
        for i in images: 
            file = fss.save(i.name, i)
            file_url = fss.url(file)
            property_media_save.append(file_url)  
            
        for ii in range(len(property_media_save)):
            image_name=property_media_save[ii]
            data.property_data[f'property_image_new_{image_name}']=image_name   
        data.save() 
    return render(request, "image.html", {'id':property_id})  
def property_status(request): 
    pass

def test_html_page(request): 
    return render(request, 'test.html') 

