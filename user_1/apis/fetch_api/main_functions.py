import json
from urllib import request
from user_1.models import Property_detail, User_register

def add_property_details_in_database(request): 
    if request.method =='POST': 
        seller_id=request.POST['user_id'] 
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
            seller_id=User_register.objects.get(user_id=seller_id), 
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
        return True 
    else: 
        return False 

def get_all_property_data(property_id=None): 
    if property_id == None: 
        my_data=Property_detail.objects.values()
        json_data=my_data[0]
        data=json.dumps(json_data, indent=4, sort_keys=True, default=str)  
    elif property_id is not None: 
        data=Property_detail.objects.get(pk=property_id) 
        # json_data=my_data[0]
        # data=json.dumps(my_data, indent=4, sort_keys=True, default=str)
    return data 

def delete_all_property_data(property_id): 
    # if request.method=='POST': 
    instance=Property_detail.objects.filter(pk=property_id) 
    instance.delete() 
    # else: 
        # print("Record is not available")
        # return False 
    return True 

def update_property_data_record(property_id): 
    instance=Property_detail.objects.filter(pk=property_id) 
    instance.save() 
    return True 