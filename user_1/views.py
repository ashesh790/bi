from urllib import request
from django.shortcuts import render
from django.urls import is_valid_path

from user_1.forms import MyForm
from user_1.models import main_seller_info 

# Render home page 
def home(request): 
    data="Hello world"
    return render(request, 'index.html', {'data':data}) 

# Login function 
def login(request): 
    return render(request, 'login.html')  

def sample(request): 
    form=MyForm()
    if request.method =='POST':
        form=MyForm(request.POST,request.FILES)
        if form.is_valid(): 
            property_title=form.cleaned_data['property_title']
            selling_option=form.cleaned_data['selling_option']
            property_desc=form.cleaned_data['property_desc']
            property_images_1=form.cleaned_data['property_images_1']
            property_images_2=form.cleaned_data['property_images_2']
            property_images_3=form.cleaned_data['property_images_3']
            property_video=form.cleaned_data['property_video'] 
            property_current_status=form.cleaned_data['property_current_status']
            property_location=form.cleaned_data['property_location']
            property_other_info=form.cleaned_data['property_other_info']
            property_media=[property_images_1,property_images_1,property_images_1,property_video] 
            # Saving data into database model 

            data=main_seller_info(
                property_title=property_title, 
                selling_option=selling_option,
                property_desc=property_desc,
                property_current_status=property_current_status,
                property_location=property_location,
                property_other_info=property_other_info,
                property_media=[property_images_1,property_images_1,property_images_1,property_video]
                )
            data.save() 
            return render(request, 'sample.html', {'form':form}) 
        else: 
            return render(request, 'sample.html', {'form':form})  
    return render(request, 'sample.html', {'form':form})