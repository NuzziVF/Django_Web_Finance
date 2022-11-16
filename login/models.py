from django.db import models
from datetime import date

# Create your models here.


class Person(models.Model):
    username = models.ForeignKey("login.Name", on_delete=models.CASCADE)
    budget = models.ForeignKey("login.Banking", on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)


class Name(models.Model):
    username = models.CharField(max_length=50)


class Banking(models.Model):
    balance = models.IntegerField()


class Banking_Changes(models.Model):
    cost = models.IntegerField()
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    user = models.ForeignKey("login.Person", on_delete=models.CASCADE)
