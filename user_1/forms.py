from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	username= forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class': 'form-control'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	phone_no = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'class': 'form-control'}))
	first_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(max_length = 20,widget=forms.TextInput(attrs={'class': 'form-control'})) 
	password1 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	class Meta:
		model = User
		fields = ['username', 'email', 'phone_no', 'password1', 'password2', 'first_name', 'last_name']


class AuthenticationForm(forms.Form):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'input-lg', 'class': 'form-control'}),
    )
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
