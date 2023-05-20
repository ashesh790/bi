import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
import requests 
import geocoder


API_KEY = "aW5ORzN6VkpJdVZrZFZSUFdlYUxxRFNpdkxVMU5kaEdzYmI5cE9hNQ==" 

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

def city_list(request): 
    country = request.GET['country_name']
    state = request.GET['state_name']
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
        return None
    

def get_location(ip_address):
    g = geocoder.ip(ip_address)
    if g.ok:
        return g.city, g.country
    else:
        return None

# Example usage
ip_address = '1.38.68.48'  # Replace with the IP address you want to geocode
location = get_location(ip_address)
if location:
    city, country = location
    print(f"City: {city}")
    print(f"Country: {country}")
else:
    print("Location not found.")
