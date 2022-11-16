from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

### All Page Views end in -Page with no spaces and first word lowercase, all Functions have underscore(_) instead of spaces and are all lowercase. Please keep this consistent.

## The if redirects if you are logged in, don't want the user to see the login again

# The variable u is used to create the name ahead of time when the account is made. This helps in displaying the name even when the person class is yet to be created.


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


### @login_required must be in front of every tab besides login and register


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("login")


### Since I am using the Model Person to keep track of all user information, and it uses ForeignKeys which requires everything to already be there, I have two renders. One will work with the Person Model, and the other will come in if the Model doesn't exist yet


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


### THIS IS A MESS, Having to order all of this in the right way is very complicated, You can't create a Person Model without all the factors already set and it requires you to fetch the others models [Name, Banking]. I have troubleshooting print statements in each path.

## The first time this page is run, it will ask for a balance/budget(path4), then it will return and user request.POST and will not display the select a budget option again(path1), finally, when you come back to the page any other times, it will run though path2 and display your current budget


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
            user = find_person(request.user)
            print("path2")
            context = {"user": user}
            return render(request, "balance.html", context)
    except Person.DoesNotExist:
        context = {"user": None}
        print("path4")
        return render(request, "balance.html", context)


### WHERE DO I EVEN START HERE, because of how many Models I have I have to order this in a particular way so that nothing is left behind when the user is deleted, the only problem is the fact that some Models can only really be identified using ones of its links in a ForeignKey. If you delete the others path first there's a change that the on_delete=models.CASCADE might not delete the remanent of some Models.

## For the most part we should't need to mess with this from know on, for the user, it should seem seamless as it deletes a user but it have to go though 3 different paths depending on when they wanted to delete their account.


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


def editPage(request):
    if request.method == "POST":
        if "edit-name-btn" in request.POST:
            name = request.POST.get("edit-name")
            n = find_name(request.user)
            u = User.objects.get(username=request.user)
            n.username = name
            u.username = name
            n.save()
            u.save()
            print(request.user)
            print("path1")
            return redirect("home")

        elif "edit-email-btn" in request.POST:
            email = request.POST.get("edit-email")
            try:
                p = find_person(request.user)
                u = User.objects.get(username=request.user)
                p.email = email
                u.email = email
                p.save()
                u.save()
                print(request.user.email)
                print("path2")
                return redirect("home")
            except Person.DoesNotExist:
                u = User.objects.get(username=request.user)
                u.email = email
                u.save()
                print(request.user.email)
                print("path3")
                return redirect("home")

    else:
        return render(request, "edit.html")


@login_required(login_url="login")
def reviewsPage(request):
    return redirect("home")


@login_required(login_url="login")
def savingsPage(request):
    return redirect("home")


@login_required(login_url="login")
def stonksPage(request):
    return redirect("home")


### Anything past here are just functions for keeping track of Models and create Models.


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
