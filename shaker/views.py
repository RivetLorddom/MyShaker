from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core import serializers
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm, AddDrinkForm
from .models import User, Drink, Category, Ingredient, Glass

import json


def pagination(drinks, request):
    # show 10 drinks per page
    paginator = Paginator(drinks, 10)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def index(request):
    all_drinks = Drink.objects.all().order_by("creator", "-name").reverse()

    # user is looking for a cocktail by name
    if request.method == "POST":
        typed = request.POST["drink_name"]
        all_drinks = Drink.objects.filter(name__icontains=typed)
        # drink_name = request.POST["drink_name"]
        # return redirect(f"/drinks/{drink_name}")

    page_obj = pagination(all_drinks, request)

    if not all_drinks:
        messages.error(request, "No drink found.")
    return render(
        request,
        "shaker/index.html",
        {"page_obj": page_obj, "categories": Category.objects.all()},
    )


@login_required
def favorites(request, username):
    user = User.objects.filter(username=username)[0]
    favorites = user.favorites.all()

    page_heading = "Your favorite drinks in one place"
    if not favorites:
        page_heading = "No drinks added to favorites yet"
    return render(
        request,
        "shaker/favorites.html",
        {"favorites": favorites, "page_heading": page_heading},
    )


def drink_page(request, drink_name):

    if request.method == "POST":
        # delete object, redirect to homepage
        drink_to_delate = Drink.objects.get(name=drink_name)
        drink_to_delate.delete()
        return redirect("/")

    # else request is GET, show the drink page
    drinks = Drink.objects.filter(name__icontains=drink_name)
    drink = drinks[0] if drinks else None
    if drink:
        return render(request, "shaker/single_drink.html", {"drink": drink})
    else:
        messages.error(request, "No drink found.")
        return redirect("/")


def luck(request):
    random_drink = Drink.objects.order_by("?")[0]

    return render(
        request,
        "shaker/single_drink.html",
        {"drink": random_drink, "page_heading": "Lucky drink for you!"},
    )


def add_drink_form(request):
    if request.method == "POST":
        form = AddDrinkForm(request.POST)
        if form.is_valid():
            new_drink = Drink()
            new_drink.creator = request.user
            new_drink.name = form.cleaned_data["name"]
            new_drink.category = Category.objects.get(
                name=form.cleaned_data["category"]
            )
            new_drink.alcoholic = not (form.cleaned_data["non_alcoholic"])
            new_drink.glass = Glass.objects.get(name=form.cleaned_data["glass"])
            new_drink.instructions = form.cleaned_data["instructions"]
            new_drink.image_url = form.cleaned_data["image_url"]
            new_drink.save()
            new_drink.ingredients.set(
                Ingredient.objects.filter(name__in=form.cleaned_data["ingredients"])
            )

            messages.success(request, "Drink added to database.")
            return redirect("/")

    # if request is GET
    form = AddDrinkForm()
    return render(request, "shaker/add_new_drink.html", {"form": form})


@login_required
def add_essentials(request):
    # view for adding ingredients, glasses and categories
    if request.method == "POST":

        # add ingredient
        if "add_ingredient" in request.POST:
            ingredient_name = request.POST["add_ingredient"]
            Ingredient(name=ingredient_name).save()
            return redirect("/add")

        # add glass
        if "add_glass" in request.POST:
            glass_name = request.POST["add_glass"]
            Glass(name=glass_name).save()
            return redirect("/add")

        # add category
        if "add_category" in request.POST:
            category_name = request.POST["add_category"]
            Category(name=category_name).save()
            return redirect("/add")

    else:
        return JsonResponse(
            {"error": "POST method required for this route"}, status=404
        )


# API for user info
@csrf_exempt
@login_required
def user_api(request, user_id):

    # Query for the user
    try:
        this_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    # return user info content
    if request.method == "GET":
        return JsonResponse(this_user.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("favorites") is not None:
            this_user.favorites.set(Drink.objects.filter(id__in=data["favorites"]))
        this_user.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse(
            {"error": "GET or PUT method required for this route"}, status=404
        )


# API for drink objects
@csrf_exempt
def drinks_api(request, drink_id):

    # Query for the drink
    try:
        this_drink = Drink.objects.get(pk=drink_id)
    except Drink.DoesNotExist:
        return JsonResponse({"error": "Drink does not exist"}, status=404)

    # return drink info content
    if request.method == "GET":
        return JsonResponse(this_drink.serialize())

    else:
        return JsonResponse({"error": "GET method required for this route"}, status=404)


# API for all drinks
@csrf_exempt
def all_drinks_api(request):
    # get list of dicts
    raw_data = serializers.serialize("python", Drink.objects.all())
    # extract the inner `fields` dicts
    actual_data = [d["fields"] for d in raw_data]
    # dump to JSON
    output = json.dumps(actual_data)
    return HttpResponse(output)


# VIEWS FOR REGISTER, LOGIN, LOGOUT


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegistrationForm()
    return render(request, "shaker/register.html", {"registration_form": form})


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
    return render(request, "shaker/login.html", {"login_form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
