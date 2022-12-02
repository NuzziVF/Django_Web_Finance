from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class Bank(forms.Form):
    balance = forms.IntegerField(required=True)


class Financing(forms.Form):
    name = forms.CharField(max_length=50, required=False)
    cost = forms.IntegerField(required=True)


class Transactions(forms.Form):
    name = forms.CharField(max_length=50, required=False)
    money = forms.IntegerField()
