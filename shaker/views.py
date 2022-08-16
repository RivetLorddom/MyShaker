from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .forms import RegistrationForm
import requests


# Create your views here.



def index(request):

    # user is looking for a cocktail by name
    if request.method == "POST":
        drink_name = request.POST["drink_name"]
        return redirect(f"/drink/{drink_name}")

    categories = [
        "Ordinary Drink",
        "Cocktail",
        "Shake",
        "Other\/Unknown",
        "Cocoa",
        "Shot",
        "Coffee \/ Tea",
        "Homemade Liqueur",
        "Punch \/ Party Drink",
        "Beer",
        "Soft Drink"
    ]

    drinks = []
    for _ in range(5):
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php').json()["drinks"][0]
        drinks.append(response)
    return render(request, "shaker/index.html", {
        "drinks": drinks,
        "categories": categories
    })

def favorites(request):
    return render(request, "shaker/favorites.html")


def drink_page(request, drink_name):
    ingredients = []
    drink = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={drink_name.lower()}').json()["drinks"][0]
    
    for field in drink:
        if field.startswith("strIngredient"):
            if drink[field] is not None:
                ingredients.append(drink[field])

    return render(request, "shaker/single_drink.html", {
    "drink": drink, 
    "ingredients": ingredients
    })


def luck(request):
    ingredients = []
    drink = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php').json()["drinks"][0]
    
    for field in drink:
        if field.startswith("strIngredient"):
            if drink[field] is not None:
                ingredients.append(drink[field])
    return render(request, "shaker/single_drink.html", {
        "drink": drink, 
        "ingredients": ingredients
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