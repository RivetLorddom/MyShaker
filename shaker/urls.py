from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("drinks/<str:drink_name>", views.drink_page, name="drink_page"),
    path("favorites/<str:username>", views.favorites, name="favorites"),
    path("luck", views.luck, name="luck"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    # path for creating new drinks
    path("add", views.add_drink_form, name="add_drink_form"),
    # path for creating new ingredients, categories, glasses
    path("add_essentials", views.add_essentials, name="add_essentials"),
    # API route for drink objects info and user info
    path("api/drinks/all", views.all_drinks_api, name="all_drinks_api"),
    path("api/drinks/<int:drink_id>", views.drinks_api, name="drinks_api"),
    path("api/users/<str:user_id>", views.user_api, name="user_api"),
]
