import json
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from user_1.apis.fetch_api.main_functions import add_property_details_in_database, delete_all_property_data, get_all_property_data, update_property_data_record
from user_1.apis.fetch_api.state_management.handle_state import login_user, signup_user
from user_1.models import User_register 
from django.core.serializers import serialize 
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
        return render(request, "login.html") 
    except Exception as ex: 
        print(f"Solve this: {ex}") 

# logout 
def logout(request): 
    if request: 
        try: 
            del request.session['user_name'] 
        except: 
            print("Logout") 
    return render(request, 'login.html') 

# Render home page 
def home(request): 
    try: 
        data="Hello world"
        return render(request, 'index.html', {'data':data})   
    except Exception as ex: 
        print(f"Solve this: {ex}") 

def add_property_details(request):    
    try:
        if request.method =='POST' and len(request.POST) is not None: 
            add_property_details_in_database(request) 
        else: 
            print("Please Fill tha all necessary fields")  
        return render(request, 'property_basic_detail.html') 
    except Exception as ex: 
        print(f"Solve this: {ex}")

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

def update_property(request, property_id): 
    try: 
        property_id=property_id
        update=update_property_data_record(property_id) 
        return render(request, 'property_basic_detail.html')  
    except Exception as ex: 
        print(f"Solve this: {ex}") 

def property_status(request): 
    pass 