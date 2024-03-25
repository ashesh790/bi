import json
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from staying_source.settings import MEDIA_ROOT, MEDIA_ROOT_USER_ICON, MEDIA_URL
from user_1.apis.fetch_api.advance_filter_functions import search_properties, user_all_details
from user_1.models import User_other_utils, p_detail_v1
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from geopy.geocoders import Nominatim


def add_property_details_in_database(request):
    if request.method == "POST" or request.method == "FILES":
        media_data = request.FILES.getlist("images")
        property_image_save = []
        property_video_save = []
        fss = FileSystemStorage()
        for i in media_data:
            file = fss.save(i.name, i)
            file_url = str(fss.url(file))
            file_url = file_url.replace("%20", " ")
            property_image_save.append(file_url)

        seller_id = request.POST["user_id"]
        property_data = {}
        property_values = dict(request.POST)
        property_values = list(property_values.keys())
        if "csrfmiddlewaretoken" in property_values:
            property_values.remove("csrfmiddlewaretoken")
        if "user_id" in property_values:
            property_values.remove("user_id")
        if "images" in property_values:
            property_values.remove("images")
        for i in property_values:
            property_data[i] = request.POST[i]
        property_data["property_image"] = property_image_save
        property_data["property_video"] = {}
        p_detail_v1.objects.create(
            seller_id=User.objects.get(pk=seller_id),
            property_data=property_data,
        )
        return True
    else:
        return False


def update_property_image(request=None, property_id=None, user_icon=None):
    if property_id == 0:
        if len(request.FILES) > 0:
            user_id = request.session["username"]
            if os.path.exists(MEDIA_ROOT_USER_ICON + user_id):
                user_icon = os.listdir(MEDIA_ROOT_USER_ICON + user_id)
                for i in range(0, len(user_icon)):
                    os.remove("media/user_icons/" + user_id + "/" + user_icon[i])
            # Create an instance of FileSystemStorage with the desired folder name
            custom_storage = FileSystemStorage(location=f"media/user_icons/{user_id}/")
            user_icon = request.FILES["file"]
            # Access the URL of the saved file
            file_url = custom_storage.url(user_icon)
            custom_storage.save(user_icon.name, user_icon)
            return "True"
        else:
            return "False"

    property_data = p_detail_v1.objects.get(id=property_id)
    if request.method == "POST":
        fss = FileSystemStorage()
        data = request.FILES.getlist("images")
        property_image_save = []
        property_video_save = []
        for i in data:
            file = fss.save(i.name, i)
            file_url = fss.url(file)
            file_url = file_url.replace("%20", " ")
            property_image_save.append(file_url)
        property_data.property_data["property_image"] = (
            property_data.property_data["property_image"] + property_image_save
        )
        property_data.save()
        return True


def get_all_property_data(property_id=None, property_type=None):
    if property_id == None:
        data = p_detail_v1.objects.values()
        data = data[0]
        data = json.dumps(data, indent=4, sort_keys=True, default=str)
    elif property_type != None:
        data = p_detail_v1.objects.filter(property_data__property_type=property_type)
    elif property_id is not None:
        data = p_detail_v1.objects.get(pk=property_id)

    number_of_item = 5
    paginator = Paginator(data, number_of_item)
    first_page = paginator.page(1).object_list
    page_range = paginator.page_range
    return data, first_page, page_range


def delete_all_property_data(property_id):
    instance = p_detail_v1.objects.get(pk=property_id)
    property_image_data = instance.property_data["property_image"]
    for i in property_image_data:
        i = i.replace("/media/", "")
        if i in os.listdir(MEDIA_ROOT):
            os.remove("media/" + i)
        else:
            print("Not found")
    instance.delete()
    return True



def delete_property_image_from_database(request, property_id, image_name):
    property_data = p_detail_v1.objects.get(id=property_id)
    property_image_data = MEDIA_URL + image_name
    property_data.property_data["property_image"].remove(property_image_data)
    if image_name in os.listdir(MEDIA_ROOT):
        os.remove("media/" + image_name)
    else:
        print("Not found")
    property_data.save()
    return True


def property_bound_data():
    data = (
        settings.BASE_DIR / "user_1" / "static" / "property_boundry_api" / "data.json"
    )
    with open(data) as f:
        data = json.load(f)
    property_data = data["property_type"]
    property_count = p_detail_v1.objects.all()
    property_c = {}
    for i in property_count:
        if i.property_data["property_type"] in property_c:
            property_c[i.property_data["property_type"]] += 1
        else:
            property_c[i.property_data["property_type"]] = 1
    return property_c


def search_property_type(request, sale_type=None, property_type=None): 
    page_number = 1 
    items_per_page = 8 
    number_of_pages = 1
    if "page_number" in request.POST:  
        page_number = request.POST["page_number"] 

    prop_data = {}
    property_type_core = "all"
    sale_type = sale_type
    if property_type is None and sale_type is None:
        if "data" in request.POST:
            property_type_core = request.POST["data"]
            if property_type_core != "all":
                property_type_core_data = p_detail_v1.objects.filter(
                    property_data__property_type=property_type_core
                )
                paginator = Paginator(property_type_core_data, items_per_page) 
                property_type_core_data = paginator.page(page_number) 
                property_type_core_data = property_type_core_data.object_list 
                number_of_pages = paginator.num_pages
                for i in property_type_core_data:
                    user_detail = user_all_details(i.id)
                    i.property_data["user_detail"] = user_detail
                    prop_data[i.id] = i.property_data
            else:
                property_type_core_data = p_detail_v1.objects.all()
                paginator = Paginator(property_type_core_data, items_per_page) 
                property_type_core_data = paginator.page(page_number)
                property_type_core_data = property_type_core_data.object_list
                number_of_pages = paginator.num_pages 
                for i in property_type_core_data:
                    user_detail = user_all_details(i.id)
                    i.property_data["user_detail"] = user_detail
                    prop_data[i.id] = i.property_data
            return JsonResponse(
                {"prop_data": prop_data, "prop_data_type": property_type_core, "number_of_pages":number_of_pages}
            )
        else: 
            property_type_core_data = p_detail_v1.objects.all()
            paginator = Paginator(property_type_core_data, items_per_page) 
            property_type_core_data = paginator.page(page_number)
            property_type_core_data = property_type_core_data.object_list
            number_of_pages = paginator.num_pages 
            for i in property_type_core_data:
                user_detail = user_all_details(i.id)
                i.property_data["user_detail"] = user_detail
                prop_data[i.id] = i.property_data
            return JsonResponse(
                {"prop_data": prop_data, "prop_data_type": property_type_core, "number_of_pages":number_of_pages}
            )
    if sale_type is not None and property_type is not None:
        if sale_type == "all":
            property_type = property_type
            data = p_detail_v1.objects.filter(property_data__property_type=property_type) 
            paginator = Paginator(data, items_per_page) 
            data = paginator.page(page_number) 
            data = data.object_list
        else:
            data = p_detail_v1.objects.filter(
                property_data__property_type=property_type
            ).filter(property_data__selling_option=sale_type)
        for i in data:
            prop_data[i.id] = i.property_data
        data = prop_data
        paginator = Paginator(data, items_per_page) 
        data = paginator.page(page_number) 
        data = data.object_list
        return data
    if sale_type == "Sale" or sale_type == "Rent":
        data = p_detail_v1.objects.filter(property_data__selling_option=sale_type)
        for i in data:
            prop_data[i.id] = i.property_data
        data = prop_data 
        paginator = Paginator(data, items_per_page) 
        data = paginator.page(page_number) 
        data = data.object_list
        return data
    elif sale_type == "all":
        data = p_detail_v1.objects.all()
        for i in data:
            prop_data[i.id] = i.property_data
        data = prop_data 
        paginator = Paginator(data, items_per_page) 
        data = paginator.page(page_number) 
        data = data.object_list
        return data
    else:
        data = p_detail_v1.objects.filter(property_data__property_type=property_type)
        paginator = Paginator(data, items_per_page) 
        data = paginator.page(page_number) 
        data = data.object_list
        return data 


def delete_all_images_from_media(property_id):
    property_data = p_detail_v1.objects.get(id=property_id)
    property_image_data = property_data.property_data["property_image"]
    for i in property_image_data:
        if i in os.listdir(MEDIA_ROOT):
            os.remove("media/" + i)
        else:
            print("Not found")
    return True



def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="MyWebApp/1.0")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.address
    address_dict = {}
    address_dict["city"] = location.raw["address"].get("city", "")
    address_dict["country"] = location.raw["address"].get("country", "")
    address_dict["state"] = location.raw["address"].get("state", "")
    address_dict["postal_code"] = location.raw["address"].get("postcode", "")
    return address_dict if location else None


def liked_and_saved_property_ids(request, user_id):
    saved_property_list = [] 
    try:
        user_data = User_other_utils.objects.get(user_id = User.objects.get(username=request.session['username'])) 
        if "saved_property" in user_data.user_other_data_json:
            for property_id in user_data.user_other_data_json["saved_property"]:
                saved_property_list.append(property_id)
        return saved_property_list
    except Exception as ex: 
        return saved_property_list


def add_like_property_count(property_id, remove_like=False):
    property_record = p_detail_v1.objects.get(id=property_id)
    if not remove_like:
        if "likes" in property_record.property_other_data:
            property_record.property_other_data["likes"] += 1
        else:
            property_record.property_other_data["likes"] = 1
        property_record.save()
        return "liked"
    else:
        if property_record.property_other_data["likes"] > 0:
            property_record.property_other_data["likes"] -= 1
            property_record.save()
            return "like_removed"


def blocked_property(request, property_details=False):
    # TODO: code remain if multile user gave same proeprty report.
    user_id = request.session["username"]
    property_utils = p_detail_v1.objects.filter(
        seller_id = User.objects.get(username=user_id)
    )
    property_id_reason = {}
    if len(property_utils) > 0:
        count = 0
        for i in property_utils:
            if "report_reason" in i.property_other_data:
                count += 1
                property_id_reason[f"{i.id}__{count}"] = i.property_other_data["report_reason"]
        data = json.dumps(property_id_reason)
        return HttpResponse(data)
    else:
        return HttpResponse("No data")


def byte_to_dict(bytes_data):
    bytes_data = bytes_data.content
    # Decode the bytes into a string
    str_data = bytes_data.decode("utf-8")

    # Parse the string into a dictionary
    dict_data = json.loads(str_data)
    return dict_data

def property_user_profile(request): 
    property_id = request.POST['property_id'] 
    data_dictionary = {}
    user_data = user_all_details(property_id) 
    user_id = user_data["user_id"]
    user_properties = user_profile_wise_property(user_id)  
    for i in user_properties: 
        data_dictionary[i.pk] = i.property_data
    data = {"data_dictionary":data_dictionary, "user_data":user_data}
    return JsonResponse(data)


def user_profile_wise_property(user_id): 
    try: 
        user_properties_list = []
        if len(user_id)>0 and user_id is not None: 
            data = p_detail_v1.objects.filter(seller_id=user_id)   
            for i in data: 
                user_properties_list.append(i)
        else: 
            return None
    except Exception as ex: 
        return None
    return user_properties_list 

def read_static_files(file_name): 
    file_path = (
            settings.BASE_DIR
            / "user_1"
            / "static"
            / "property_boundry_api"
            / file_name
        ) 
    with open(file_path) as f:
        file_data = json.load(f)
    return file_data 

def is_field_verified(primary_key): 
    user = User_other_utils.objects.get(pk=primary_key)
    if user.is_email_verified: 
        return 1
    return 0
