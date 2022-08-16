from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .forms import RegistrationForm
import requests

from .models import User, Drink, Category, Ingredient, Glass


# =====
# Getting database prepopulated:
from .models import Drink
import json

def prepopulate():
    with open('drink_data.json', encoding='utf-8') as data_file:
        json_data = json.loads(data_file.read())

        for drink_data in json_data["drinks"]:
            drink = Drink.create(**drink_data)
       
# =====


# Create your views here.



def index(request):

    # user is looking for a cocktail by name
    if request.method == "POST":
        drink_name = request.POST["drink_name"]
        return redirect(f"/drinks/{drink_name}")

    random_drinks = Drink.objects.order_by('?')[0:10]

    return render(request, "shaker/index.html", {
        "drinks": random_drinks,
        "categories": Category.objects.all()
    })

def favorites(request):
    return render(request, "shaker/favorites.html")


def drink_page(request, drink_name):
    drink = Drink.objects.filter(name__icontains=drink_name)[0]
        
    return render(request, "shaker/single_drink.html", {
    "drink": drink
    })


def luck(request):
    random_drink = Drink.objects.order_by('?')[0]
    
    return render(request, "shaker/single_drink.html", {
        "drink": random_drink
    })




# VIEWS FOR REGISTER, LOGIN, LOGOUT

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegistrationForm()
    return render (request, "shaker/register.html", {"registration_form":form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        messages.error(request, "Invalid username or password.")

    # if request is GET or logging in failed
    form = AuthenticationForm()
    return render(request, "shaker/login.html", {"login_form":form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))