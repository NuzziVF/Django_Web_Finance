"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    # register and login are the only ones that don't require you to log in first
    path("register/", registerPage, name="register"),
    path("login/", loginPage, name="login"),
    # All of these will redirect back to login if used before logging in.
    path("", homePage, name="home"),
    path("balance/", balancePage, name="bal"),
    # These next few are not finished yet so they redirect to home
    path("past_reviews/", reviewsPage, name="reviews"),
    path("savings/", savingsPage, name="savings"),
    path("stocks/", stonksPage, name="stonks"),
    # Careful with these two, they will delete or logout if even typed in the url
    path("logout/", logoutUser, name="logout"),
    path("delete/", deleteUser, name="delete"),
    path("edit/", editPage, name="edit"),
]
