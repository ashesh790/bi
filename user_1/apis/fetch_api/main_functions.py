import json
import os
from urllib import request
from django.conf import settings
from django.http import HttpResponse, JsonResponse 

from staying_source.settings import MEDIA_ROOT, MEDIA_URL
from user_1.models import User_register, p_detail
from django.core.files.storage import FileSystemStorage

def add_property_details_in_database(request): 
    if request.method =='POST' or request.method == 'FILES': 
        media_data=request.FILES.getlist('images')
        property_image_save=[] 
        property_video_save=[]
        fss = FileSystemStorage()
        for i in media_data: 
            file = fss.save(i.name, i)
            file_url = str(fss.url(file)) 
            file_url = file_url.replace("%20", ' ')
            property_image_save.append(file_url)

        seller_id=request.POST['user_id'] 
        property_data={} 
        property_data['property_type']=request.POST['property_type'] 
        property_data['property_age']=request.POST['property_age'] 
        property_data['selling_option']=request.POST['selling_option'] 
        property_data['construction_status']=request.POST['construction_status'] 
        property_data['floor']=request.POST['floor']
        property_data['bhk']=request.POST['bhk']  
        property_data['bathroom']=request.POST['bathroom'] 
        property_data['balcony']=request.POST['balcony'] 
        property_data['furnish_type']=request.POST['furnish_type'] 
        property_data['geography_area']=request.POST['geography_area'] 
        property_data['parking_type']=request.POST['parking_type'] 
        property_data['property_value']=request.POST['property_value'] 
        property_data['property_rent_price']=request.POST['property_rent_price'] 
        property_data['from_avail_property_date']=request.POST['from_avail_property_date'] 
        property_data['country']=request.POST['country'] 
        property_data['state']=request.POST['state']
        property_data['city']=request.POST['city']
        property_data['property_address']=request.POST['property_address'] 
        property_data['property_image']= property_image_save
        property_data['property_video']= {}  
        # fetching last property detail from databases  
        property_detail=p_detail.objects.create(
            seller_id=User_register.objects.get(user_id=seller_id), 
            property_data=property_data,  
        )
        return True 
    else: 
        return False 

def update_property_image(request, property_id): 
    user_id=request.session['user_id'] 
    property_data=p_detail.objects.get(id=property_id)
    if request.method =="POST": 
        data=request.FILES.getlist('images')
        property_image_save=[] 
        property_video_save=[]
        fss = FileSystemStorage()
        for i in data: 
            file = fss.save(i.name, i)
            file_url = fss.url(file) 
            file_url = file_url.replace("%20", " ") 
            property_image_save.append(file_url)  
        property_data.property_data['property_image'] = property_data.property_data['property_image'] + property_image_save  
        property_data.save() 
        return True
    
def get_all_property_data(property_id=None, property_type=None): 
    if property_id == None: 
        my_data=p_detail.objects.values()
        json_data=my_data[0]
        data=json.dumps(json_data, indent=4, sort_keys=True, default=str)  
    elif property_type != None: 
        data = p_detail.objects.filter(property_data__property_type=property_type)
    elif property_id is not None: 
        data=p_detail.objects.get(pk=property_id) 
    return data 

def delete_all_property_data(property_id): 
    # if request.method=='POST': 
    instance=p_detail.objects.filter(pk=property_id) 
    instance.delete() 
    return True 

def update_property_data_record(property_id): 
    # update will be here 
    data=p_detail.objects.get(id=property_id)   
    if request.method =='POST' or request.method == 'FILES': 
        pass 
    return data      

def delete_property_image_from_database(request, property_id, image_name): 
    property_data=p_detail.objects.get(id=property_id) 
    property_image_data= MEDIA_URL + image_name
    property_data.property_data['property_image'].remove(property_image_data) 
    if image_name in os.listdir(MEDIA_ROOT): 
        os.remove("media/"+image_name) 
    else: 
        print("Not found") 
    property_data.save() 
    return True 

def property_bound_data(): 
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
        # property_c[i.property_data["property_type"]] = i.property_data["property_type"]  
    return property_c

def search_property_type(request, sale_type = None, property_type = None): 
    prop_data={} 
    sale_type = sale_type 
    print(sale_type) 
    if property_type is None and sale_type is None: 
        if (request.POST['data']): 
            property_type_core = request.POST["data"] 
            if property_type_core != "all":
                property_type_core_data = p_detail.objects.filter(property_data__property_type=property_type_core) 
                for  i in property_type_core_data: 
                    prop_data[i.id] = i.property_data
            else: 
                property_type_core_data = p_detail.objects.all()  
                for  i in property_type_core_data: 
                    prop_data[i.id] = i.property_data 
            return JsonResponse(prop_data)  

    if (sale_type is not None and property_type is not None): 
        if (sale_type == "all"): 
            property_type = property_type
            data = p_detail.objects.filter(property_data__property_type=property_type)
        else: 
            data = p_detail.objects.filter(property_data__property_type=property_type).filter(property_data__selling_option=sale_type)
        for i in data:
            prop_data[i.id]=i.property_data
        data=prop_data  
        return data
    if (sale_type == "Sale" or sale_type == "Rent"): 
        data = p_detail.objects.filter(property_data__selling_option=sale_type) 
        for i in data:
            prop_data[i.id]=i.property_data
        data=prop_data  
        return data  
    elif(sale_type == "all"): 
        data = p_detail.objects.all() 
        for i in data:
            prop_data[i.id]=i.property_data
        data=prop_data  
        return data
    else:
        data = p_detail.objects.filter(property_data__property_type=property_type) 
        # data=data[0].property_data 
        return data 