from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    favorites = models.ManyToManyField("Drink", related_name="favorited_by", default=None, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "favorites": [favorite.id for favorite in self.favorites.all()]
        }


class Drink(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    alcoholic = models.BooleanField(default=True)
    category =  models.ForeignKey("Category", on_delete=models.CASCADE, related_name="related_listings", null=True, blank=True)
    glass = models.ForeignKey("Glass", on_delete=models.CASCADE, related_name="used_for", null=True, blank=True)
    ingredients = models.ManyToManyField("Ingredient", related_name="used_for", blank=True)
    instructions = models.CharField(max_length=3000)
    image_url = models.URLField(default=None, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('drink-detail', kwargs={'pk': self.pk})

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # "creator": self.creator.username,
            "alcoholic": self.alcoholic,
            "category": self.category.name,
            "glass": self.glass.name,
            "ingredients": [ingredient.name for ingredient in self.ingredients.all()],
            "instructions": self.instructions
        }


    # Method for creating the objects from 3rd party json format 
    @classmethod
    def create(cls, **kwargs):

        category_name = kwargs['strCategory']
        categ, created = Category.objects.get_or_create(name=category_name.title())
        
        glass_name = kwargs['strGlass']
        gl, created = Glass.objects.get_or_create(name=glass_name.title())

        alco = kwargs['strAlcoholic']
        if alco == 'Alcoholic':
            alco = True
        else:
            alco = False
        
        drink = cls.objects.create(
            name = kwargs['strDrink'],
            instructions = kwargs['strInstructions'],
            image_url = kwargs['strDrinkThumb'],
            category = categ,
            glass = gl,
            alcoholic = alco
        )

        for i in range(1, 11):
            ingr_name = kwargs[f'strIngredient{i}']
            if ingr_name:
                ingr, created = Ingredient.objects.get_or_create(name=ingr_name.title())
                drink.ingredients.add(ingr)

        return drink
    


class Category(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name


class Glass(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    class Meta:
        verbose_name_plural = "glasses"

    def __str__(self):
        return self.name
