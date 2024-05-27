from django.contrib.auth.models import User
from django import forms


class registerform(forms.Form):
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()


class loginform(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())

class employeeform(forms.Form):
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    








