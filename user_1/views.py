from urllib import request
from django.shortcuts import render

# Render home page 
def home(request): 
    data="Hello world"
    return render(request, 'index.html', {'data':data}) 

# Login function 
def login(request): 
    return render(request, 'login.html')  