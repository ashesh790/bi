import json
from urllib import request

from pymediainfo import MediaInfo
from django.http import HttpResponse
from user_1.models import User_register, p_detail
from django.core.files.storage import FileSystemStorage
from django.template import loader

def add_property_details_in_database(request): 
    if request.method =='POST' or request.method == 'FILES': 
        media_data=request.FILES.getlist('images')
        property_image_save=[] 
        property_video_save=[]
        fss = FileSystemStorage()
        for i in media_data: 
            file = fss.save(i.name, i)
            file_url = fss.url(file)
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

def upload_property_image(request, property_id): 
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
            property_image_save.append(file_url)  
        property_data.property_data['property_image'].append(property_image_save) 
        property_data.save() 
def get_all_property_data(property_id=None): 
    if property_id == None: 
        my_data=p_detail.objects.values()
        json_data=my_data[0]
        data=json.dumps(json_data, indent=4, sort_keys=True, default=str)  
    elif property_id is not None: 
        data=p_detail.objects.get(pk=property_id) 
        # json_data=my_data[0]
        # data=json.dumps(my_data, indent=4, sort_keys=True, default=str)
    return data 

def delete_all_property_data(property_id): 
    # if request.method=='POST': 
    instance=p_detail.objects.filter(pk=property_id) 
    instance.delete() 
    # else: 
        # print("Record is not available")
        # return False 
    return True 

def update_property_data_record(property_id): 
    # update will be here 
    data=p_detail.objects.get(id=property_id)   
    if request.method =='POST' or request.method == 'FILES': 
        pass 
    return data      