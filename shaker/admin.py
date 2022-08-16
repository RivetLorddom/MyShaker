from django.contrib import admin
from .models import User, Drink, Category, Glass, Ingredient

class DrinkAdmin(admin.ModelAdmin):
    filter_horizontal = ("ingredients",)

# Register your models here.
admin.site.register(User)
admin.site.register(Drink, DrinkAdmin)
admin.site.register(Category)
admin.site.register(Glass)
admin.site.register(Ingredient)