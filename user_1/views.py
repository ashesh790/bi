from email import message
from urllib import request
from django.shortcuts import render

from user_1.models import Property_detail
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
        property_type=request.POST['property_type'] 
        property_age=request.POST['property_age'] 
        selling_option=request.POST['selling_option'] 
        construction_status=request.POST['construction_status'] 
        floor=request.POST['floor']
        bhk=request.POST['bhk']  
        bathroom=request.POST['bathroom'] 
        balcony=request.POST['balcony'] 
        furnish_type=request.POST['furnish_type'] 
        geography_area=request.POST['geography_area'] 
        parking_type=request.POST['parking_type'] 
        property_value=request.POST['property_value'] 
        property_rent_price=request.POST['property_rent_price'] 
        from_avail_property_date=request.POST['from_avail_property_date'] 
        property_address=request.POST['property_address'] 

        property_detail=Property_detail.objects.create(
            property_type=property_type,
            property_age=property_age,
            selling_option=selling_option, 
            construction_status=construction_status,
            floor=floor,
            bhk=bhk,
            bathroom=bathroom,
            balcony=balcony,
            furnish_type=furnish_type,
            geography_area=geography_area,
            parking_type=parking_type, 
            property_value=property_value,
            property_rent_price=property_rent_price, 
            from_avail_property_date=from_avail_property_date, 
            property_address=property_address
        )
        message.success(request,'Data has been submitted')
    return render(request, 'property_basic_detail.html') 

def show_property_detail(request): 
    pass 

def delete_property(request): 
    pass 

def property_status(request): 
    pass 