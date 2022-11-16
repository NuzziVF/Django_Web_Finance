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
    try:
        user = find_person(request.user)
        context = {"user": user}
        return render(request, "home.html", context)
    except Person.DoesNotExist:
        user = find_name(request.user)

        context = {"user": None}
        print(user)
        return render(request, "home.html", context)


@login_required(login_url="login")
def balancePage(request):
    try:
        if request.method == "POST":
            balance = request.POST.get("bal")
            bal = create_bal(balance)
            print("path1")
            person = create_person(find_name(request.user), bal, request.user.email)
            context = {"bal": bal, "user": person}
            return render(request, "balance.html", context)
        else:
            print("path2")
            user = find_person(request.user)
            context = {"user": user}
            return render(request, "balance.html", context)
    except Person.DoesNotExist:
        context = {"user": None}
        print("path4")
        return render(request, "balance.html", context)


@login_required(login_url="login")
def deleteUser(request):
    if request.method == "POST":
        username = request.user
        print(request.POST.get("username"))
        u = User.objects.get(username=username)
        u.delete()
        messages.success(request, "The user is deleted")
        return redirect("login")
    else:
        try:
            print(request.user)
            name = Name.objects.get(username=request.user)
            person = Person.objects.get(username=name)
            bank = Person.objects.get(username=name).budget
            bal = bank.balance
            bank = Banking.objects.get(balance=bal)
            u = User.objects.get(username=request.user)
            bank.delete()
            person.delete()
            name.delete()
            u.delete()
            messages.success(request, "The user has been deleted")
            return redirect("login")
        except Person.DoesNotExist:
            name = Name.objects.get(username=request.user)
            u = User.objects.get(username=request.user)
            name.delete()
            u.delete()
            messages.success(request, "The user has been deleted")
            return redirect("login")


@login_required(login_url="login")
def reviewsPage(request):
    return redirect("home")


@login_required(login_url="login")
def savingsPage(request):
    return redirect("home")


@login_required(login_url="login")
def stonksPage(request):
    return redirect("home")


def create_name(name):
    u = Name(username=name)
    u.save()
    return u


def create_bal(bal):
    b = Banking(balance=bal)
    b.save()
    return b


def create_person(user, bal, mail):
    p = Person(username=user, budget=bal, email=mail)
    p.save()
    return p


def find_name(name):
    n = Name.objects.get(username=name)
    return n


def find_person(name):
    search_name = Name.objects.get(username=name)
    p = Person.objects.get(username=search_name)
    return p
