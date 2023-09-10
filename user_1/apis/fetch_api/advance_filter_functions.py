import json
import pandas as pd
from django.db.models import Q
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from user_1.apis.fetch_api.country_api import country_list
from django.core import serializers
from django.http import JsonResponse
from user_1.models import User_register, p_detail
from django.core.paginator import Paginator


def advance_filter_boundary(request):
    data = (
        settings.BASE_DIR / "user_1" / "static" / "property_boundry_api" / "data.json"
    )
    # country = country_list(request)
    # country = json.loads(country)
    with open(data) as f:
        data = json.load(f)

        # data = {"data": data, "country": country} 
        data = {"data": data}
        return JsonResponse(data)


def search_properties(request, address_dict=None, reload_location=None): 
    page_number = request.POST['page_number'] 
    if len(page_number) == 0: 
        page_number = 1
    if reload_location is not None:
        address_dict = {"place_name": address_dict}
        if address_dict is not None:
            property_details = address_dict
    else:
        property_details = request.POST["search_object"]
        property_details = json.loads(property_details)
        if "property_type" in property_details:
            if (
                property_details["property_type"] == "all"
                or property_details["property_type"] == "All"
            ):
                property_details.pop("property_type")
        if "selling_option" in property_details:
            if (
                property_details["selling_option"] == "all"
                or property_details["selling_option"] == "All"
            ):
                property_details.pop("selling_option")
    query = Q()
    for field, value in property_details.items():
        if field == "place_name":
            query &= Q(**{"property_data__place_name__icontains": value})
        elif field == "property_type":
            query &= Q(**{"property_data__property_type__icontains": value})
        else:
            if value:
                query &= Q(**{"property_data__" + field: value})

    search_results = p_detail.objects.filter(query) 
    paginator = Paginator(search_results, 10) 
    page = paginator.get_page(page_number)
    page_data = page.object_list
    if reload_location is not None:
        if search_results is not None:
            return search_results
    else:
        user_details = []
        if page_data:
            search_results = pd.DataFrame(page_data.values())
            property_ids = list(search_results["id"].values)
            for i in property_ids:
                user_basic_details = user_all_details(request, i)
                user_details.append(json.dumps(user_basic_details)) 
            search_results["user_data"] = pd.DataFrame(user_details)
            search_results = search_results.to_dict() 
            total_pages =  paginator.num_pages
            return JsonResponse({"search_results":search_results, "has_next":page.has_next(), "total_pages":total_pages})
        else:
            return HttpResponse(None)


def user_all_details(request, property_id):
    try:
        data = p_detail.objects.get(id=property_id)
        user_id = data.seller_id.pk
        user_data = User_register.objects.get(pk=user_id)
        user_email = user_data.user_email
        user_name = user_data.user_name
        user_mobile = user_data.user_mobile
        user_gender = user_data.user_gender
        saller_data = {
            "user_email": user_email,
            "user_name": user_name,
            "user_mobile": user_mobile,
            "user_gender": user_gender,
        }

        return saller_data
    except Exception as ex:
        print(ex)


def search_properties_by_string(request):
    search_string = request.POST["search_string"]
    search_results = p_detail.objects.filter(
        Q(property_data__property_type__icontains=search_string)
        | Q(property_data__property_name__icontains=search_string)
        | Q(property_data__property_address__icontains=search_string)
        | Q(property_data__property_city__icontains=search_string)
        | Q(property_data__property_state__icontains=search_string)
        | Q(property_data__property_country__icontains=search_string)
        | Q(property_data__property_zip__icontains=search_string)
        | Q(property_data__property_description__icontains=search_string)
        | Q(property_data__property_price__icontains=search_string)
        | Q(property_data__property_area__icontains=search_string)
        | Q(property_data__property_bedrooms__icontains=search_string)
        | Q(property_data__property_bathrooms__icontains=search_string)
        | Q(property_data__property_garage__icontains=search_string),
    )
    return "pass"
