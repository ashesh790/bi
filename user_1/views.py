import json
import requests
from django.conf import settings
from django.core.files.storage import default_storage
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from staying_source.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL
from user_1.apis.fetch_api.advance_filter_functions import advance_filter_boundary, search_properties
from user_1.apis.fetch_api.country_api import property_type_list, country_list, state_list, city_list
from user_1.apis.fetch_api.main_functions import add_property_details_in_database, delete_all_property_data, delete_property_image_from_database, get_all_property_data, property_bound_data, search_property_type, update_property_data_record, update_property_image
from user_1.apis.fetch_api.state_management.handle_state import login_user, signup_user 
from user_1.models import User_register, p_detail 
from django.core.serializers import serialize 
import shutil 
from django.core.files.storage import FileSystemStorage
# from user_1.forms import MyForm

# Note: Create login and signup in single html page 

def advance_filter(request): 
    property_data = p_detail.objects.all() 
    boundry_data = advance_filter_boundary(request) 
    boundry_data = json.loads(boundry_data.content) 
    return render(request, "advance_filter/filter.html", {"boundry_data":boundry_data['data'], "country":boundry_data['country'], "property_data":property_data}) 
# Login function 
def sign_up(request): 
    if request.method =="POST": 
        user_name=request.POST['user_name']
        user_email=request.POST['user_email'] 
        user_mobile=request.POST['user_number'] 
        user_psw=request.POST['user_psw'] 
        user_name.lower()
        user_email.lower()
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
        login_status = login_user(request) 
        if login_status is not False:   
            return render(request, 'theme/index.html') 
        else: 
            return redirect('Invalid Credentials') 
    else: 
        return render(request, "theme/login.html")
# logout 
def logout(request): 
    if request: 
        try: 
            del request.session['user_name'] 
        except: 
            print("Logout") 
    return render(request, 'theme/login.html') 
 
def add_property_details(request):    
    try:
        if request.method =='POST' and len(request.POST) is not None: 
            property_details=add_property_details_in_database(request) 
        country_name_list = country_list(request) 
        country_name_list = json.loads(country_name_list) 
        data = settings.BASE_DIR / "user_1" / "static" / "property_boundry_api" / "data.json"  
        with open(data) as f:
            data = json.load(f)  
        data = data 
        return render(request, 'admin/admin2/add_property.html', {
            "property_type":data["property_type"], 
            "deal_option":data["deal_option"],
            "construction_status":data["construction_status"], 
            "furnish_type":data["furnish_type"], 
            "bhk_details":data["bhk_details"], 
            "bathroom_details":data["bathroom_details"],
            "balcony_details":data["balcony_details"], 
            "parking_details":data["parking_details"], 
            "country_name_list": country_name_list
            })  
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
        return render(request,'admin/admin2/add_property.html') 
    except Exception as ex: 
        print(f"Solve this: {ex}") 
    return render(request,'admin/admin2/add_property.html')

def update_property(request, property_id=0): 
    # postData = request.get_json()
    try: 
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if request.method == 'POST': 
            media_data=request.FILES.getlist('images')
            data=p_detail.objects.get(id=property_id)
            property_id=property_id 
            property_image_save=[] 
            property_video_save=[]
            fss = FileSystemStorage() 
            if len(media_data) >0 and media_data is not None:
                for i in media_data: 
                    file = fss.save(i.name, i)
                    file_url = fss.url(file)
                property_image_save.append(file_url) 
                property_data['property_image']= property_image_save
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
            data.property_data['country'] = request.POST['data[property_country]'] 
            data.property_data['state'] = request.POST['data[property_state]']
            data.property_data['city'] = request.POST['data[property_city]'] 
            data.property_data['property_address'] = request.POST['data[property_address]'] 
            data.save()  
            return render(request, 'admin/admin2/update_property.html', {'data':data, "id":property_id})
        property_id=property_id
        data=p_detail.objects.get(id=property_id) 
        property_data=data.property_data
        return render(request, 'admin/admin2/update_property.html', {'data':property_data, "id":property_id})
    except Exception as ex: 
        print(f"Solve this: {ex}") 
    return render(request, 'admin/admin2/update_property.html', {'data':property_data, "id":property_id})  

def manage_image_upload(request,property_id): 
    update_property_image(request, property_id) 
    return redirect(f'/update_property_record/{property_id}')  

def delete_property_image(request,property_id, image_name): 
    delete_property_image_from_database(request, property_id, image_name) 
    return redirect(f'/update_property_record/{property_id}') 
def property_status(request): 
    pass

def test_html_page(request): 
    return render(request, 'test.html') 

def prop_table(request): 
    user_id= User_register.objects.get(user_id=request.session._session['user_id']) 
    # count for user inquiries 
    # user_inq_len = len(user_id.user_other_data['inquiry_dtl']) 
    data=p_detail.objects.filter(seller_id=user_id)
    return render(request, 'admin/admin2/prop_table.html', {'data':data}) 

################################################## userside functions ################################

def dashboard(request): 
    user_id= User_register.objects.get(user_id=request.session._session['user_id']) 
    # count for user inquiries 
    # user_inq_len = len(user_id.user_other_data['inquiry_dtl']) 
    data=p_detail.objects.filter(seller_id=user_id) 
    return render(request, 'admin/admin2/dashboard.html', {'data':data, #'user_inq_len':user_inq_len
                                                           })  

def crud_property(request): 
    data=p_detail.objects.filter(seller_id=User_register.objects.get(user_id=request.session._session['user_id']))  
    return render(request, 'record.html', {'data':data}) 
# Render home page 

def home(request): 
    property_category=property_bound_data 
    property_data = p_detail.objects.all() 
    return render(request, 'theme/index.html', {'property_category':property_category, 'property_data':property_data})  
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

def print_property_type(request): 
    data = settings.BASE_DIR / "user_1" / "static" / "property_boundry_api" / "data.json"  
    with open(data) as f:
        data = json.load(f)  
    property_data = data['property_type'] 
    property_count = p_detail.objects.all() 
    property_c={} 
    for i in property_count: 
        if i.property_data["property_type"] in property_c: 
            property_c[i.property_data["property_type"]]+=1
        else:
            property_c[i.property_data["property_type"]]=1 
    return render(request, 'theme/property-type.html', {"property_c":property_c}) 

def property_list(request): 
    return render(request, 'theme/property-list.html') 

def property_category_wise(request, property_type):
    sale_type = None  
    data = search_property_type(request, sale_type, property_type) 
    # search_property_type(request, sale_type, property_type = None) 
    return render(request, 'theme/property-category-wise.html', {'data':data, 'property_type':property_type}) 

def property_sell_option_wise(request): 
    sale_type = request.POST['selling_option']
    try:
        property_type = request.POST['property_type'] 
    except: 
        data = search_property_type(request, sale_type, property_type = None)
        property_type = None 
    if (property_type is not None): 
        data = search_property_type(request, sale_type, property_type) 
    # if (len(data) != 0): 
    #     return HttpResponse(json.dumps({"empty_message":f"There is no any property like '{property_type}' with 'For {sale_type}' "}))    
    return HttpResponse(json.dumps({"data":data})) 

def show_full_property_detail(request, property_id): 
    property_data = p_detail.objects.all()
    data = p_detail.objects.get(id=property_id)
    data = data.property_data 
    return render(request, 'theme/property-detail-page.html', {'data':data, 'property_id':property_id, 'property_data':property_data}) 

def property_post_modal_management(request): 
    sale_type = request.POST['p_dtl_btn_val'] 
    property_id = request.POST['property_id'] 
    if (sale_type == "saller_detail"): 
        data = p_detail.objects.get(id=property_id) 
        user_id = data.seller_id.pk 
        user_data = User_register.objects.get(pk=user_id) 
        user_email = user_data.user_email 
        user_name = user_data.user_name 
        user_mobile = user_data.user_mobile 
        user_gender = user_data.user_gender 
        saller_data = {
            "Saller email":user_email,
            "Saller name":user_name,
            "Saller mobile":user_mobile, 
            "Saller gender":user_gender
        }
        return HttpResponse(json.dumps({"saller_data":saller_data})) 
    elif(sale_type == "save_post"): 
        pass 
    elif(sale_type == "share_post"):
        pass 
    elif(sale_type == "submit_btn_dc"): 
        property_id = request.POST['property_id'] 
        sender_name = request.POST['sender_name'] 
        sender_mobile = request.POST['sender_mobile'] 
        sender_email = request.POST['sender_email'] 
        description = request.POST['description'] 
        inquiry_dtl={
            "property_id":property_id,
            "sender_name":sender_name,
            "sender_mobile":sender_mobile,
            "sender_email":sender_email,
            "description":description
        }
        # inquiry_dtl = json.dumps(inquiry_dtl) 
        data = p_detail.objects.get(id=property_id) 
        user_id = data.seller_id.pk
        save_data = User_register.objects.get(pk=user_id) 
        user_data = save_data.user_other_data 
        if (user_data is not None or len(user_data) !=0): 
            # user_data = json.loads(user_data) 
            user_data['inquiry_dtl'].append(inquiry_dtl) 
            save_data.user_other_data = user_data 
        else: 
            user_data = {"inquiry_dtl":[inquiry_dtl]}
            # user_data = json.dumps(user_data) 
            save_data.user_other_data = user_data
        save_data.save()
    return HttpResponse(json.dumps({"sale_type":sale_type}))  

def inquiries_from_user(request): 
    user_data = User_register.objects.get(user_id=request.session._session['user_id']) 
    user_data = user_data.user_other_data 
    return HttpResponse(json.dumps({"user_data":user_data}))















# Test functions  
def test_function(request):
    return render(request, 'admin/admin2/index.html')  