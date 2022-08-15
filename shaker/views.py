from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from .forms import RegistrationForm


# Create your views here.


def index(request):
    return render(request, "shaker/index.html")

def favorites(request):
    return HttpResponse("my favorites")




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
            messages.success(request, "Logged in.")
            return redirect("/")
        messages.error(request, "Invalid username or password.")

    # if request is GET or logging in failed
    form = AuthenticationForm()
    return render(request, "shaker/login.html", {"login_form":form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))