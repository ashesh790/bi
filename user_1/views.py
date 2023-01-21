from urllib import request
from django.shortcuts import render
from django.urls import is_valid_path

from user_1.forms import MyForm 

# Render home page 
def home(request): 
    data="Hello world"
    return render(request, 'index.html', {'data':data}) 

# Login function 
def login(request): 
    return render(request, 'login.html')  

def sample(request): 
    if request.method =='POST':
        form = MyForm(request.POST)
        if form.is_valid:
            first_value = form.cleaned_data["property_title"]
            form.save()
        else: 
            form.save()
            print("Data is not cleaned")
    form=MyForm()  
    return render(request, 'sample.html', {'form':form})