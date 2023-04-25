import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from user_1.apis.fetch_api.country_api import country_list, fetch_country

from user_1.models import p_detail 
def advance_filter_boundary(request): 
    data = settings.BASE_DIR / "user_1" / "static" / "property_boundry_api" / "data.json" 
    country = country_list(request) 
    country = json.loads(country) 
    with open(data) as f:
        data = json.load(f) 
    
        data = {"data":data, "country":country} 
        return JsonResponse(data) 

def filtered_property_as_per_query(request):  
    # Subquery exmple 
    # ids = Employee.objects.filter(company='Private').values_list('id', flat=True) 
    # Person.objects.filter(id__in=ids).values('name', 'age')
    # Search query will be like below: 
    query={
        "property_type": "Residential", 
        "property_data": {
            "property_type": "Flat",
            "property_for": "Sale",
            "property_location": "Kolkata",
            "property_area": "1000",
            "property_price": "1000000",
            "property_bedroom": "2",
            "property_bathroom": "2",
            "property_furnished": "Unfurnished",
            "property_parking": "1",
            "property_floor": "2",
            "property_age": "5",
            "property_availability": "Ready to move",
            "property_status": "Active",
        },
    } 
    property_type = query['property_type'] 
    property_data = query['property_data']  
    property_data = p_detail.objects.filter(
        property_type=property_type, 
        property_data__property_type=property_data['property_type'], 
        property_data__property_for=property_data['property_for'], 
        property_data__property_location=property_data['property_location'], 
        property_data__property_area=property_data['property_area'], 
        property_data__property_price=property_data['property_price'], 
        property_data__property_bedroom=property_data['property_bedroom'], 
        property_data__property_bathroom=property_data['property_bathroom'], 
        property_data__property_furnished=property_data['property_furnished'], 
        property_data__property_parking=property_data['property_parking'], 
        property_data__property_floor=property_data['property_floor'], 
        property_data__property_age=property_data['property_age'], 
        property_data__property_availability=property_data['property_availability'], 
        property_data__property_status=property_data['property_status']
        )
    property_data_dict ={} 
    search_type = {} 
    property_type = request.POST.get('property') 
    property_data = p_detail.objects.filter(property_data__property_type=property_type)
    for i in property_data: 
        property_data_dict[i.id] = i.property_data  
    return JsonResponse(property_data_dict) 
