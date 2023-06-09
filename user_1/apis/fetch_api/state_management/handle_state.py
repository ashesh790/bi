from urllib import request
from django.contrib import messages
from django.shortcuts import redirect
from user_1.models import User_register


def signup_user(request): 
    if request.method =="POST": 
        user_name=request.POST['user_name'] 
        user_email=request.POST['user_email'] 
        user_mobile=request.POST['user_number'] 
        user_gender=request.POST['user_gender'] 
        user_psw=request.POST['user_psw'] 

        if User_register.objects.filter(user_name=user_name): 
            print("Existing User!") 
            messages.error(request, "Username must be under 20 charcters!!") 
            return redirect("login") 
        if User_register.objects.filter(user_email=user_email).exists():
            print("Email is already exist!") 
            return redirect("login") 
        if len(user_name)>20: 
            print("USer must be under 20 character") 
            return redirect("login") 
        if not user_name.isalnum(): 
            print("User name must be alphanumeric") 
            return redirect("login") 
        
        new_user=User_register.objects.create(user_name=user_name, user_email=user_email, user_mobile=user_mobile, user_gender=user_gender, user_psw=user_psw) 
        if new_user == True: 
            return redirect('login') 
        else: 
            return False 

def login_user(request): 
    try: 
        if request.method=="POST": 
            user_name=request.POST['data[name]'] 
            user_psw=request.POST['data[email]'] 
            latitude = request.POST['data[latitude]']
            longitude = request.POST['data[longitude]'] 
            # if User_register.objects.filter(user_name=user_name).exists():
            location_number = {
                "latitude":latitude, 
                "longitude":longitude
            }
            if User_register.objects.filter(user_name=user_name).exists():
                login=User_register.objects.filter(user_name=user_name) 
                request.session['user_name']=user_name 
                user_id=login[0].user_id 
                login_user=User_register.objects.get(user_id=user_id) 
                request.session['user_id']=user_id  
                # login_user.user_other_data['location_number'] = location_number 
                login_user.save()
                return True 
            else: 
                return False 
    except Exception as ex: 
        print(f"Solve this: {ex}") 
        return False
