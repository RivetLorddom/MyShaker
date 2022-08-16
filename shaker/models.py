from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    favorites = models.ManyToManyField("Drink", related_name="favorited_by", default=None, blank=True)


class Drink(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True)
    name = models.CharField(max_length=50)
    alcoholic = models.BooleanField(default=True)
    category =  models.ForeignKey("Category", on_delete=models.CASCADE, related_name="related_listings", default=None)
    glass = models.ForeignKey("Glass", on_delete=models.CASCADE, related_name="used_for", default=None)
    ingredients = models.ManyToManyField("Ingredient", related_name="used_for", default=None)
    instructions = models.CharField(max_length=3000)
    image_url = models.URLField(default=None, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Glass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
