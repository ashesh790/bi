import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse

from user_1.models import p_detail 
def advance_filter_boundary(request): 
    data = settings.BASE_DIR / "user_1" / "static" / "property_boundry_api" / "data.json" 
    with open(data) as f:
        data = json.load(f) 
    
        data = {"data":data}
        return JsonResponse(data)   

def filtered_property_as_per_query(request): 
    property_data_dict ={} 
    property_type = request.POST.get('property')
    property_data = p_detail.objects.filter(property_data__property_type=property_type)
    for i in property_data: 
        property_data_dict[i.id] = i.property_data  
    return JsonResponse(property_data_dict) 