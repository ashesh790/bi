from django import forms 
from .models import main_seller_info 
# Create your models here.
class MyForm(forms.Form):
    a = forms.ImageField(max_length=20)
    mat = forms.CharField(max_length=200)