from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("drinks/<str:drink_name>", views.drink_page, name="drink_page"),
    path("favorites", views.favorites, name="favorites"),
    path("luck", views.luck, name="luck"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]