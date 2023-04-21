import json
from django.conf import settings
from django.http import JsonResponse
import requests 


def fetch_country(request): 
    # country API 
    url = "https://api.first.org/data/v1/countries" 
    country_list= [] 
    response = requests.get(url)
    if response.status_code == 200:
        # Success!
        data = response.json()
        countrys = data['data'] 
        for country in countrys: 
            country_list.append(data['data'][country]['country']) 
        data = {"country_list":country_list} 
        return JsonResponse(data)  
    else:
        # Something went wrong
        print(f"Error: {response.status_code}")


def property_type_list(request): 
    data = settings.BASE_DIR / "user_1" / "static" / "property_boundry_api" / "data.json" 
    with open(data) as f: 
        data = json.load(f) 
    property_type_list = []
    for property_type in data ['property_type']:
        property_type_list.append(property_type) 
    data = {"property_type_list":property_type_list}
    return JsonResponse(data)