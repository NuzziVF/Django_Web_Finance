from django.db import models
from datetime import date, datetime

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
    name = models.CharField(null=True, max_length=50)
    cost = models.IntegerField()
    date_added = models.DateTimeField(default=datetime.now, blank=True, null=True)
    user = models.ForeignKey("login.Person", on_delete=models.CASCADE)


class Stock(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    adjusted_close = models.FloatField()
    volume = models.FloatField()
    dividend_amount = models.FloatField()
    split_coefficient = models.FloatField()
