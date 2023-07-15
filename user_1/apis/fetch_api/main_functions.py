import json
import os
from urllib import request
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from staying_source.settings import MEDIA_ROOT, MEDIA_ROOT_USER_ICON, MEDIA_URL
from user_1.apis.fetch_api.advance_filter_functions import search_properties
from user_1.models import User_register, p_detail, property_utility
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
        # fetching last property detail from databases
        property_detail = p_detail.objects.create(
            seller_id=User_register.objects.get(user_id=seller_id),
            property_data=property_data,
        )
        return True
    else:
        return False


def update_property_image(request=None, property_id=None, user_icon=None):
    if property_id == 0:
        if len(request.FILES) > 0:
            user_id = request.session["user_id"]
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

    property_data = p_detail.objects.get(id=property_id)
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
        data = p_detail.objects.values()
        data = data[0]
        data = json.dumps(data, indent=4, sort_keys=True, default=str)
    elif property_type != None:
        data = p_detail.objects.filter(property_data__property_type=property_type)
    elif property_id is not None:
        data = p_detail.objects.get(pk=property_id)

    number_of_item = 5
    paginator = Paginator(data, number_of_item)
    first_page = paginator.page(1).object_list
    page_range = paginator.page_range
    return data, first_page, page_range


def delete_all_property_data(property_id):
    # if request.method=='POST':
    instance = p_detail.objects.get(pk=property_id)
    property_image_data = instance.property_data["property_image"]
    for i in property_image_data:
        i = i.replace("/media/", "")
        if i in os.listdir(MEDIA_ROOT):
            os.remove("media/" + i)
        else:
            print("Not found")
    instance.delete()
    return True


def update_property_data_record(property_id):
    # update will be here
    data = p_detail.objects.get(id=property_id)
    if request.method == "POST" or request.method == "FILES":
        pass
    return data


def delete_property_image_from_database(request, property_id, image_name):
    property_data = p_detail.objects.get(id=property_id)
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
    property_count = p_detail.objects.all()
    property_c = {}
    for i in property_count:
        if i.property_data["property_type"] in property_c:
            property_c[i.property_data["property_type"]] += 1
        else:
            property_c[i.property_data["property_type"]] = 1
        # property_c[i.property_data["property_type"]] = i.property_data["property_type"]
    return property_c


def search_property_type(request, sale_type=None, property_type=None):
    prop_data = {}
    sale_type = sale_type
    print(sale_type)
    if property_type is None and sale_type is None:
        if request.POST["data"]:
            property_type_core = request.POST["data"]
            if property_type_core != "all":
                property_type_core_data = p_detail.objects.filter(
                    property_data__property_type=property_type_core
                )
                for i in property_type_core_data:
                    user_detail = user_all_details(request, i.id)
                    i.property_data["user_detail"] = user_detail
                    prop_data[i.id] = i.property_data
            else:
                property_filter = "all"
                property_type_core_data = p_detail.objects.all()
                for i in property_type_core_data:
                    user_detail = user_all_details(request, i.id)
                    i.property_data["user_detail"] = user_detail
                    prop_data[i.id] = i.property_data
            return JsonResponse(
                {"prop_data": prop_data, "prop_data_type": property_type_core}
            )

    if sale_type is not None and property_type is not None:
        if sale_type == "all":
            property_type = property_type
            data = p_detail.objects.filter(property_data__property_type=property_type)
        else:
            data = p_detail.objects.filter(
                property_data__property_type=property_type
            ).filter(property_data__selling_option=sale_type)
        for i in data:
            prop_data[i.id] = i.property_data
        data = prop_data
        return data
    if sale_type == "Sale" or sale_type == "Rent":
        data = p_detail.objects.filter(property_data__selling_option=sale_type)
        for i in data:
            prop_data[i.id] = i.property_data
        data = prop_data
        return data
    elif sale_type == "all":
        data = p_detail.objects.all()
        for i in data:
            prop_data[i.id] = i.property_data
        data = prop_data
        return data
    else:
        data = p_detail.objects.filter(property_data__property_type=property_type)
        # data=data[0].property_data
        return data


def delete_all_images_from_media(property_id):
    property_data = p_detail.objects.get(id=property_id)
    property_image_data = property_data.property_data["property_image"]
    for i in property_image_data:
        if i in os.listdir(MEDIA_ROOT):
            os.remove("media/" + i)
        else:
            print("Not found")
    return True


def save_location(request):
    if "user_id" not in request.session:
        return HttpResponse("Do Login")
    user_id = request.session["user_id"]
    latitude = request.POST["data[latitude]"]
    longitude = request.POST["data[longitude]"]
    location_number = {"latitude": latitude, "longitude": longitude}
    request.session["location_number"] = location_number
    login_user = User_register.objects.get(user_id=user_id)
    request.session["user_id"] = user_id
    login_user.user_other_data["location_number"] = location_number
    login_user.save()
    return HttpResponse("Location saved")


def show_property_location_wise(request):
    location_fetched = ""
    reload_location = True
    latitude = request.session["location_number"]["latitude"]
    longitude = request.session["location_number"]["longitude"]
    address_dict = get_location_name(latitude, longitude)
    if address_dict is not None or len(address_dict) > 0:
        if address_dict["city"] != "" and address_dict["city"] is not None:
            location_fetched = address_dict["city"]
        elif address_dict["state"] != "" and address_dict["state"] is not None:
            location_fetched = address_dict["state"]
        elif address_dict["country"] != "" and address_dict["country"] is not None:
            location_fetched = address_dict["country"]
    property = search_properties(request, location_fetched, reload_location)
    return property, location_fetched
    # data = p_detail.objects.all()
    # property_data = {}
    # for i in data:
    #     property_data[i.id] = i.property_data
    # return JsonResponse({"property_data":property_data, "latitude":latitude, "longitude":longitude})


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


def liked_and_saved_property_ids(user_id):
    saved_property_list = []
    liked_property_list = []
    user_id = user_id
    user_data = User_register.objects.get(user_id=user_id)
    if "saved_property" in user_data.user_other_data:
        for property_id in user_data.user_other_data["saved_property"]:
            saved_property_list.append(property_id)
    if "liked_property" in user_data.user_other_data:
        for liked_property in user_data.user_other_data["liked_property"]:
            liked_property_list.append(liked_property)
        return saved_property_list, liked_property_list
    else:
        return saved_property_list, liked_property_list


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


def add_like_property_count(property_id, remove_like=False):
    property_record = p_detail.objects.get(id=property_id)
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
    # code remain if multile user gave same proeprty report.
    user_id = request.session["user_id"]
    property_utils = property_utility.objects.filter(
        seller_id=User_register.objects.get(user_id=user_id)
    )
    property_id_reason = {}
    if len(property_utils) > 0:
        for i in property_utils:
            property_id_reason[i.property_id.id] = i.property_report["report_reason"]
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
