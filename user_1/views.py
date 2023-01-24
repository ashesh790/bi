from urllib import request
from django.shortcuts import render
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
    if request.method =='POST': 
        property_type=request.POST.get['property_type'] 
        property_age=request.POST.get['property_age'] 
        selling_option=request.POST.get['selling_option'] 
        construction_status=request.POST.get['construction_status'] 
        floor=request.POST.get('floor') 
        bhk=request.POST.get['bhk']  
        bathroom=request.POST.get['bathroom'] 
        balcony=request.POST.get['balcony'] 
        furnish_type=request.POST.get['furnish_type'] 
        geography_area=request.POST.get['geography_area'] 
        parking_type=request.POST.get['parking_type'] 
        property_value=request.POST.get['property_value'] 
        property_rent_price=request.POST.get['property_rent_price'] 
        from_avail_property_date=request.POST.get['from_avail_property_date'] 
        property_address=request.POST.get['property_address'] 
        
    return render(request, 'property_basic_detail.html') 

def show_property_detail(request): 
    pass 

def delete_property(request): 
    pass 

def property_status(request): 
    pass 