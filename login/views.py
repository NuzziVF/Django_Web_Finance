from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                u = create_name(user)
                messages.success(request, f"Account was created for {user}")
                return redirect("login")

        context = {"form": form}
        return render(request, "register.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        context = {}
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username OR Password was incorrect")
                return render(request, "login.html", context)

        return render(request, "login.html", context)


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def homePage(request):

    context = {"name": request.user}
    return render(request, "home.html", context)


@login_required(login_url="login")
def balancePage(request):
    if request.method == "POST":
        balance = request.POST.get("bal")
        bal = create_bal(balance)
        context = {"bal": bal}
        person = create_person(find_name(request.user), bal)
        return render(request, "balance.html", context)
    return render(request, "balance.html")


def create_name(name):
    u = Name(username=name)
    u.save()
    return u


def create_bal(bal):
    b = Banking(balance=bal)
    b.save()
    return b


def create_person(user, bal):
    p = Person(username=user, budget=bal)
    p.save()
    return p


def find_name(name):
    n = Name.objects.get(username=name)
    return n


def find_person(name):
    search_name = Name.objects.get(username=name)
    p = Person.objects.get(username=search_name)
    return p
