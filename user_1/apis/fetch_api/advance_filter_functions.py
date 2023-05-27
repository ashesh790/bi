import json
import pandas as pd 
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from user_1.apis.fetch_api.country_api import country_list

from user_1.models import p_detail 
def advance_filter_boundary(request): 
    data = settings.BASE_DIR / "user_1" / "static" / "property_boundry_api" / "data.json" 
    country = country_list(request) 
    country = json.loads(country) 
    with open(data) as f:
        data = json.load(f) 
    
        data = {"data":data, "country":country} 
        return JsonResponse(data) 

def search_properties(request): 
    property_details = request.POST['search_object'] 
    property_details = json.loads(property_details) 
    if (property_details['property_type'] == "all" or property_details['property_type'] == "All"):
        property_details.pop("property_type")
    
    if(property_details['selling_option'] == "all" or property_details['selling_option'] == "All"): 
        property_details.pop("selling_option")
    query = Q()
    for field, value in property_details.items():
        if value:
            query &= Q(**{"property_data__"+field: value})
    
    search_results = p_detail.objects.filter(query) 
    if search_results.exists():   
        search_results = pd.DataFrame(search_results.values())
        search_results = search_results.to_dict()
        return JsonResponse(search_results)
    else:
        return HttpResponse("No data found")
