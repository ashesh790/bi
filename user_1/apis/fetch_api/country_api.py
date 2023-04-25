import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import requests 

API_KEY = "aW5ORzN6VkpJdVZrZFZSUFdlYUxxRFNpdkxVMU5kaEdzYmI5cE9hNQ==" 

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
        return data 
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

# Country, state and city API functions 
def country_list(request):
    url = f"https://api.countrystatecity.in/v1/countries" 
    headers = {
    'X-CSCAPI-KEY': API_KEY
    }
    response = requests.request("GET", url, headers=headers) 
    if (response.status_code == 200): 
        return response.text
    else:
        # Something went wrong
        print(f"Server Busy")

def state_list(request): 
    country = request.GET['country_name']
    url = f"https://api.countrystatecity.in/v1/countries/{country}/states" 
    headers = {
    'X-CSCAPI-KEY': API_KEY
    }
    response = requests.request("GET", url, headers=headers) 
    if (response.status_code == 200): 
        return HttpResponse(response.text)
    else:
        # Something went wrong
        print(f"Server Busy") 

def city_list(request, country, state):
    url = f"https://api.countrystatecity.in/v1/countries/{country}/states/{state}/cities" 
    headers = {
    'X-CSCAPI-KEY': API_KEY
    }
    response = requests.request("GET", url, headers=headers) 
    if (response.status_code == 200):
        return HttpResponse(response.text) 
    else:
        # Something went wrong
        print(f"Server Busy") 