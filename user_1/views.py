import json
from venv import logger
from numpy import generic
import pyotp
import requests
import re
import pandas as pd
from django.conf import settings
from django.core.files.storage import default_storage
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from staying_source.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL 
from django.contrib.auth import logout
from django.core.mail import send_mail

# from user_1.apis.REST_API.database import (
#     p_detail_api,
#     specific_property,
#     user_wise_property,
# )
from user_1.apis.fetch_api.advance_filter_functions import (
    advance_filter_boundary,
    search_properties,
)
from user_1.apis.fetch_api.country_api import (
    property_type_list,
    country_list,
    state_list,
    city_list,
)
from user_1.apis.fetch_api.main_functions import (
    add_like_property_count,
    add_property_details_in_database,
    blocked_property,
    byte_to_dict,
    delete_all_property_data,
    delete_property_image_from_database,
    get_all_property_data,
    get_location_name,
    liked_and_saved_property_ids,
    read_static_files,
    search_property_type,
    update_property_image,
    user_all_details,
    property_user_profile,
)
from user_1.forms import UserRegisterForm
from user_1.models import OTP, User_other_utils, p_detail_v1
from django.core.serializers import serialize
import shutil
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from allauth.socialaccount.models import SocialAccount

# Note: Create login and signup in single html page


def advance_filter(request):
    try:
        property_data = p_detail_v1.objects.all()
        boundry_data = advance_filter_boundary(request)
        boundry_data = json.loads(boundry_data.content)
        return render(
            request,
            "advance_filter/filter.html",
            {
                "boundry_data": boundry_data["data"],
                "country": boundry_data["country"],
                "property_data": property_data,
            },
        )
    except Exception as ex:
        return render(request, "theme/404.html")


# sign up
def login_app(request):
    try:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session["username"] = username
                request.session["pk"] = user.pk
                form = login(request, user)
                return redirect("home")
        form = AuthenticationForm() 
        return render(request, "auth_app/login.html", {"form": form, "title": "log in"})
    except Exception as ex:
        raise ex 


# logout
def logout_view(request):
    try:
        if request:
            try:
                del request.session["username"]
                del request.session["pk"]
                request.session.clear()
                request.session.flush()
                logout(request)
            except Exception as ex:
                raise ex 
        return redirect("login")
    except Exception as ex:
        return render(request, "theme/404.html")


def add_property_details(request):
    try:
        if "pk" not in request.session:
            return redirect("/login")
        if request.method == "POST" and len(request.POST) is not None:
            property_details = add_property_details_in_database(request)
        # country_name_list = country_list(request)
        # country_name_list = json.loads(country_name_list)
        data = read_static_files("data.json")

        return render(
            request,
            "theme/add_property.html",
            {
                "property_type": data["property_type"],
                "deal_option": data["deal_option"],
                "construction_status": data["construction_status"],
                "furnish_type": data["furnish_type"],
                "bhk_details": data["bhk_details"],
                "bathroom_details": data["bathroom_details"],
                "balcony_details": data["balcony_details"],
                "parking_details": data["parking_details"],
                "add_property_details": "add_property_page",
            },
        )
    except Exception as ex: 
        logger.error(ex)
        return render(request, "theme/404.html")


def show_property_detail(request, property_id):
    try:
        property_id = property_id
        data, first_page, page_range = get_all_property_data(property_id=property_id)
        template = loader.get_template("show_property_detail.html")
        context = {"data": data, "first_page": first_page, "page_range": page_range}
        return HttpResponse(template.render(context, request))
    except Exception as ex:
        return render(request, "theme/404.html")


def delete_property(request, property_id):
    try:
        # country_name_list = country_list(request)
        # country_name_list = json.loads(country_name_list)
        data = read_static_files("data.json")
        property_id = property_id
        delete_all_property_data(property_id)
        return render(
            request,
            "theme/add_property.html",
            {
                "property_type": data["property_type"],
                "deal_option": data["deal_option"],
                "construction_status": data["construction_status"],
                "furnish_type": data["furnish_type"],
                "bhk_details": data["bhk_details"],
                "bathroom_details": data["bathroom_details"],
                "balcony_details": data["balcony_details"],
                "parking_details": data["parking_details"],
                "add_property_details": "add_property_page",
            },
        )
    except Exception as ex:
        (request, "theme/404.html")
    return render(
        request,
        "theme/add_property.html",
        {
            "property_type": data["property_type"],
            "deal_option": data["deal_option"],
            "construction_status": data["construction_status"],
            "furnish_type": data["furnish_type"],
            "bhk_details": data["bhk_details"],
            "bathroom_details": data["bathroom_details"],
            "balcony_details": data["balcony_details"],
            "parking_details": data["parking_details"],
            "add_property_details": "add_property_page",
        },
    )


def update_property(request, property_id=0):
    # postData = request.get_json()
    try:
        bondry_data = read_static_files("data.json")
        is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"
        if request.method == "POST":
            media_data = request.FILES.getlist("images")
            data = p_detail_v1.objects.get(id=property_id)
            property_id = property_id
            property_image_save = []
            property_video_save = []
            fss = FileSystemStorage()
            if len(media_data) > 0 and media_data is not None:
                for i in media_data:
                    file = fss.save(i.name, i)
                    file_url = fss.url(file)
                property_image_save.append(file_url)
                property_data["property_image"] = property_image_save
            property_values = dict(request.POST)
            property_values = list(property_values.keys())
            property_values.remove("csrfmiddlewaretoken")
            property_values.remove("id")
            for i in property_values:
                column_name = i
                column_name = i.replace("data[", "")
                column_name = column_name.replace("]", "")
                data.property_data[column_name] = request.POST[i]
            data.save()
            return render(
                request, "theme/update_property.html", {"data": data, "id": property_id}
            )
        property_id = property_id
        data = p_detail_v1.objects.get(id=property_id)
        property_data = data.property_data

        return render(
            request,
            "theme/update_property.html",
            {
                "data": property_data,
                "id": property_id,
                "property_type": bondry_data["property_type"],
                "deal_option": bondry_data["deal_option"],
                "construction_status": bondry_data["construction_status"],
                "furnish_type": bondry_data["furnish_type"],
                "bhk_details": bondry_data["bhk_details"],
                "bathroom_details": bondry_data["bathroom_details"],
                "balcony_details": bondry_data["balcony_details"],
                "parking_details": bondry_data["parking_details"],
            },
        )
    except Exception as ex:
        print(f"Solve this: {ex}")
    return render(
        request,
        "theme/update_property.html",
        {"data": property_data, "id": property_id},
    )


def manage_image_upload(request, property_id=None):
    user_icon = update_property_image(request, property_id)
    if user_icon == "True" or user_icon == "False":
        return redirect("/update_profile")
    return redirect(f"/update_property_record/{property_id}")


def delete_property_image(request, property_id, image_name):
    delete_property_image_from_database(request, property_id, image_name)
    return redirect(f"/update_property_record/{property_id}")


def property_status(request):
    pass


def test_html_page(request):
    return render(request, "test.html")


def prop_table(request):
    user_id = User.objects.get(pk=request.session["pk"])
    # count for user inquiries
    # user_inq_len = len(user_id.user_other_data['inquiry_dtl'])
    data = p_detail_v1.objects.filter(seller_id=user_id)
    return render(
        request,
        "theme/prop_table.html",
        {"data": data, "property_table": "property_table"},
    )


################################################## userside functions ################################


def dashboard(request):
    if "username" not in request.session:
        return redirect("/login")
    user_id = User.objects.get(username=request.session["username"])
    # count for user inquiries
    # user_inq_len = len(user_id.user_other_data['inquiry_dtl'])
    data = p_detail_v1.objects.filter(seller_id=user_id)
    return render(
        request,
        "theme/dashboard.html",
        {"data": data, "dashboard_page": "dashboard_page"},
    )


def crud_property(request):
    data = p_detail_v1.objects.filter(
        seller_id=User.objects.get(pk=request.session["pk"])
    )
    return render(request, "record.html", {"data": data})


# Render home page
def home(request):
    try: 
        if "pk" not in request.session: 
            try: 
                user_id = request.session["_auth_user_id"]
                is_auth = User.objects.get(
                pk=user_id
                ) 
                user_data = {
                "username": is_auth.username,
                "email": is_auth.email,
                } 
                request.session["username"] = user_data["username"]
                request.session["pk"] = is_auth.pk
            except Exception as ex: 
                return redirect("login")
        page_number = request.GET.get("page")
        if page_number is None:
            page_number = 1
        saved_property_list = ""
        if "pk" in request.session:
            user_id = request.session["pk"]
            saved_property_list = liked_and_saved_property_ids(request, user_id)
        boundry_data = read_static_files("data.json")
        return render(
            request,
            "theme/index.html",
            {
                "boundry_data": boundry_data,
                "saved_property_list": saved_property_list,
            },
        )
    except Exception as ex:
        print(ex)
        return render(request, "theme/404.html")


def about_us(request):
    try:
        return render(request, "theme/about.html")
    except Exception as ex:
        return render(request, "theme/404.html")


def contact(request):
    try:
        return render(request, "theme/contact.html")
    except Exception as ex:
        return render(request, "theme/404.html")


def property_agent(request):
    try:
        return render(request, "theme/property-agent.html")
    except Exception as ex:
        return render(request, "theme/404.html")


def solve_property_issue(request):
    try:
        if request.method == "POST":
            property_id = request.POST["property_id"]
            property_issue = request.POST["property_issue"]
            if "property_issue_desc" in request.POST:
                property_issue_desc = request.POST["property_issue_desc"]
            property_data = p_detail_v1.objects.get(id=property_id)
        blocked_property_list = blocked_property(request, True)
        blocked_property_list = byte_to_dict(blocked_property_list)
        return render(request, "theme/issue.html")
    except Exception as ex:
        return render(request, "theme/404.html")


def print_property_type(request):
    try:
        data = read_static_files("data.json")
        property_data = data["property_type"]
        property_count = p_detail_v1.objects.all()
        property_c = {}
        for i in property_count:
            if i.property_data["property_type"] in property_c:
                property_c[i.property_data["property_type"]] += 1
            else:
                property_c[i.property_data["property_type"]] = 1
        return render(
            request, "theme/new_listed_property.html", {"property_c": property_c}
        )
    except Exception as ex:
        return render(request, "theme/404.html")


def property_list(request):
    try:
        return render(request, "theme/property-list.html")
    except Exception as ex:
        return render(request, "theme/404.html")


def property_category_wise(request, property_type):
    try:
        sale_type = None
        data = search_property_type(request, sale_type, property_type)
        # search_property_type(request, sale_type, property_type = None)
        return render(
            request,
            "theme/property-category-wise.html",
            {"data": data, "property_type": property_type},
        )
    except Exception as ex:
        return render(request, "theme/404.html")


def property_sell_option_wise(request):
    try:
        sale_type = request.POST["selling_option"]
        try:
            property_type = request.POST["property_type"]
        except:
            data = search_property_type(request, sale_type, property_type=None)
            property_type = None
        if property_type is not None:
            data = search_property_type(request, sale_type, property_type)
        # if (len(data) != 0):
        #     return HttpResponse(json.dumps({"empty_message":f"There is no any property like '{property_type}' with 'For {sale_type}' "}))
        return HttpResponse(json.dumps({"data": data}))
    except Exception as ex:
        return render(request, "theme/404.html")


def show_full_property_detail(request, property_id):
    try:
        data = p_detail_v1.objects.get(id=property_id)
        data = data.property_data
        return render(
            request,
            "theme/property-detail-page.html",
            {"data": data, "property_id": property_id},
        )
    except Exception as ex:
        print(ex)
        return render(request, "theme/404.html")


def inquiries_from_user(request):
    try:
        user_data = User_other_utils.objects.filter(
            user_id=User.objects.get(pk=request.session["pk"])
        )
        user_data = user_data.user_other_data
        return HttpResponse(json.dumps({"user_data": user_data}))
    except Exception as ex:
        return render(request, "theme/404.html")


# Test functions
def test_function(request):
    boundry_data = advance_filter_boundary(request)
    boundry_data = json.loads(boundry_data.content)
    return render(
        request, "theme/master_filter.html", {"boundry_data": boundry_data["data"]}
    )


def bookmark_property_detail(request):
    try:
        if "pk" not in request.session:
            raise Exception
        user_id = request.session["username"]
        property_id = request.POST["property_id"]
        try:
            user_other_data = User_other_utils.objects.get(
                user_id=User.objects.get(username=request.session["username"])
            )
        except Exception as ex:
            user_other_data = User_other_utils.objects.create(
                user_id=User.objects.get(username=user_id),
                user_other_data_json={},
            )
        removed_property = (
            True if "remove_saved_property" in list(request.POST) else False
        )
        if not removed_property:
            if "saved_property" in user_other_data.user_other_data_json:
                if (
                    property_id
                    in user_other_data.user_other_data_json["saved_property"]
                ):
                    user_other_data.user_other_data_json["saved_property"].remove(
                        property_id
                    )
                    user_other_data.save()
                    return HttpResponse("Removed")
            if user_other_data is not None:
                # user_data.user_other_data["saved_property"].append(property_id)
                if "saved_property" not in user_other_data.user_other_data_json:
                    user_other_data.user_other_data_json["saved_property"] = [
                        property_id
                    ]
                else:
                    user_other_data.user_other_data_json["saved_property"].append(
                        property_id
                    )
                    saved_property_list = user_other_data.user_other_data_json[
                        "saved_property"
                    ]
                    user_other_data.user_other_data_json["saved_property"] = list(
                        set(saved_property_list)
                    )
                user_other_data.save()
                return HttpResponse("saved")
        else:
            if property_id in user_other_data.user_other_data_json["saved_property"]:
                user_other_data.user_other_data_json["saved_property"].remove(
                    property_id
                )
                user_other_data.save()
            remaining_property = saved_property(request, True)
            if remaining_property.content == "Empty":
                return HttpResponse("Empty")
            else:
                return HttpResponse(remaining_property.content)
    except Exception as ex:
        raise ex


def google_map(request):
    try:
        return render(request, "theme/google_map.html")
    except Exception as ex:
        return render("theme/404.html")


def saved_property(request, remaining_property=False):
    try:
        saved_property_dict = {}
        if "pk" not in request.session:
            return redirect("/login")
        user_id = request.session["pk"]
        try:
            user_data = User_other_utils.objects.get(
                user_id=User.objects.get(pk=user_id)
            )
            if "saved_property" in user_data.user_other_data_json:
                saved_property_list = user_data.user_other_data_json["saved_property"]
            else:
                context = {"saved_property_dict": "null"}
                return render(request, "theme/saved_proper.html", context)
            for i in saved_property_list:
                try:
                    query_data = p_detail_v1.objects.get(id=i)
                except Exception as ex:
                    saved_property_list.remove(i)
                    continue
                saved_property_dict[i] = query_data.property_data
                saved_property_dict[i]['user_data'] = ((user_all_details(i)))
            user_data.user_other_data_json["saved_property"] = saved_property_list
            user_data.save()
            if remaining_property:
                if len(saved_property_dict) > 0:
                    return HttpResponse(
                        json.dumps({"saved_property_dict": saved_property_dict})
                    )
                else:
                    return HttpResponse("Empty")
            else:
                context = {"saved_property_dict": saved_property_dict}
                return render(request, "theme/saved_proper.html", context)
        except Exception as ex:
            context = {"saved_property_dict": saved_property_dict}
            return render(request, "theme/saved_proper.html", context)

    except Exception as ex:
        print(ex)
        return render(request, "theme/404.html")


def update_profile(request):
    user_id = request.session["username"]
    try:
        user_data = User_other_utils.objects.get(
            user_id=User.objects.get(username=user_id)
        )
    except Exception as ex:
        user_data = User_other_utils.objects.create(
            user_id=User.objects.get(username=user_id),
            user_other_data_json={},
        )
    user_record = User.objects.get(username=user_id)
    user_detail = {
        "user_id": user_id,
        "user_name": user_data.user_id.username,
        "user_email": user_data.user_id.email,
        "user_mobile": user_data.user_mobile
    }
    if "user_icon" in user_data.user_other_data_json:
        user_detail["user_icon"] = user_data.user_other_data_json["user_icon"]
    if "user_location" in user_data.user_other_data_json:
        user_detail["user_location"] = (
            user_data.user_other_data_json["user_location"],
        )
    if request.method == "POST":
        if request.content_type == "application/json":
            data = json.loads(request.body)
            user_record.username = data.get("user_name")
            user_record.email = data.get("user_email")
            if len(data["user_icon"]) > 0:
                user_icon = str(data.get("user_icon"))
                user_icon = user_icon.replace("C:\\fakepath\\", "")
                user_data.user_other_data_json["user_icon"] = user_icon
            if len(data["user_location"]) > 0:
                user_data.user_other_data_json["user_location"] = data.get(
                    "user_location"
                )
                request.session["user_location"] = data.get("user_location")
                request.session["username"] = data.get("user_name")
            user_data.user_mobile = data['user_mobile']
            user_record.save()
            user_data.save()
            return JsonResponse({"Hello": "Hello"})
    if "user_location" in user_data.user_other_data_json:
        user_detail["user_location"] = user_detail["user_location"][0]
    context = {"user_detail": user_detail}
    return render(request, "theme/profile.html", context)


def add_like_by_user(request):
    if "user_id" not in request.session:
        raise ValueError
    property_id = request.POST["property_id"]
    user_id = request.session["user_id"]
    user_data = User_other_utils.objects.filter(user_id=User.objects.get(pk=user_id))
    if "liked_property" in user_data.user_other_data:
        if property_id in user_data.user_other_data["liked_property"]:
            user_data.user_other_data["liked_property"].remove(property_id)
            status = add_like_property_count(property_id, True)
        else:
            user_data.user_other_data["liked_property"].append(property_id)
            status = add_like_property_count(property_id, False)
        user_data.save()
        return HttpResponse(status)
    else:
        user_data.user_other_data["liked_property"] = [property_id]
        status = add_like_property_count(property_id, False)
        user_data.save()
        return HttpResponse(status)


def submit_report_form(request):
    try:
        if "pk" not in request.session:
            return HttpResponse("false")
        report_data = dict()
        if request.method == "POST":
            if request.content_type == "application/json":
                data = json.loads(request.body)
                property_id = p_detail_v1.objects.get(id=data["property_id"])
                seller_id = property_id.seller_id
                property_report = {
                    "report_reason": data["report_reason"],
                    "report_desc": data["report_desc"],
                }
                property_data = p_detail_v1.objects.get(id=data["property_id"])
                property_data.seller_id=seller_id
                property_data.property_other_data=property_report
                property_data.save()
                return JsonResponse({"status": "success"})
    except Exception as ex:
        raise ex 


def user_public_profile(request, property_id):
    saved_property_list = liked_property_list = []
    user_data = user_all_details(property_id)
    boundry_data = advance_filter_boundary(request)
    boundry_data = json.loads(boundry_data.content)
    if "user_id" in request.session:
        user_id = request.session["user_id"]
        saved_property_list, liked_property_list = liked_and_saved_property_ids(
            request, user_id
        )
    return render(
        request,
        "theme/user_public_profile.html",
        {
            "user_data": user_data,
            "boundry_data": boundry_data["data"],
            "saved_property_list": saved_property_list,
            "liked_property_list": liked_property_list,
        },
    )


def save_location(request):
    if "username" not in request.session:
        return HttpResponse("Do Login")
    user_id = request.session["username"]
    latitude = request.POST["data[latitude]"]
    longitude = request.POST["data[longitude]"]
    location_number = {"latitude": latitude, "longitude": longitude}
    request.session["location_number"] = location_number
    try:
        login_user = User_other_utils.objects.get(
            user_id=User.objects.get(username=user_id)
        )
    except Exception as ex:
        login_user = User_other_utils.objects.create(
            user_id=User.objects.get(username=user_id),
            user_other_data_json={},
        )
    login_user.user_other_data_json["location_number"] = location_number
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


def google_login(request):
    return render(request, "theme/login_google.html")


def register_app(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid(): 
            # TODO : Send user to welcome mail 
            ######################### mail system #################################### 
            # username = form.cleaned_data.get('username')
			# email = form.cleaned_data.get('email')
			# htmly = get_template('email.html')
			# d = { 'username': username }
			# subject, from_email, to = 'welcome', 'your_email@gmail.com', email
			# html_content = htmly.render(d)
			# msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
			# msg.attach_alternative(html_content, "text/html")
			# msg.send()
            form.save() 
            user_data = {}  
            User_other_utils.objects.create(
                user_id=User.objects.get(username=form.cleaned_data['username']),
                user_other_data_json=user_data,
                user_mobile = form.cleaned_data['phone_no'],
                is_brocker = form.cleaned_data['is_brocker']
            )
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                request.session["username"] = form.cleaned_data['username']
                request.session["email"] = form.cleaned_data['email']
                request.session["pk"] = user.pk
                form = login(request, user)
                return redirect("home")
            messages.success(
                request, f"Your account has been created ! You are now able to log in"
            )   
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(
        request, "auth_app/register.html", {"form": form, "title": "register here"}
    )


def google_callback(request):
    try:
        social_account = SocialAccount.objects.get(
            user=request.user.id, provider="google"
        )
        user_data = {
            "username": social_account.user.username,
            "email": social_account.user.email,
            # Add other user data fields as needed
        }
        request.session["username"] = user_data["username"]
        request.session["pk"] = social_account.pk
        return redirect("home")
    except Exception as ex:
        # Handle the case where the user is not associated with a Google account
        raise ex

def send_otp_mail(request):
    if request.method == 'POST':
        response = HttpResponse()
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            return render(request, 'send_otp.html', {'message': 'Email not found'}) 

        # Generate OTP secret
        otp_secret = pyotp.random_base32()

        # Save OTP secret to the database
        otp_obj, created = OTP.objects.get_or_create(user=user, email=email)
        otp_obj.otp_secret = otp_secret
        otp_obj.save()

        # Generate OTP
        otp = pyotp.TOTP(otp_secret, interval=30)
        otp_code = otp.now()

        # Send OTP via email
        subject = 'Your OTP for Login'
        message = f'Your OTP for login is: {otp_code}'
        from_email = 'asheshtparmar@gmail.com'  # Update with your email
        recipient_list = [email]
        if send_mail(subject, message, from_email, recipient_list): 
            request.session['user_otp'] = str(otp_code)

        return HttpResponse({"status": "success"})

    else:
        return render(request, 'send_otp.html')
            

def verify_otp_mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp_code = request.POST.get('otp') 
        otp_obj = OTP.objects.filter(email=email).first()
        session_otp = request.session['user_otp']
        if not otp_obj:
            return render(request, 'verify_otp.html')  

        if session_otp == otp_code:
            print("Verified")
            otp_obj.is_verified = True
            otp_obj.save()
            return HttpResponse("200")
        else:
            return render(request, 'auth_app/register_app.html')  
    else:
        return render(request, 'auth_app/register_app.html.html')  

def login_v2(request):
    return render(request, "auth_app/register_app")