from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Category, Glass, Ingredient
from django.contrib.admin import widgets

# Create your forms here.

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user



class AddDrinkForm(forms.Form):

    
    all_categories = [(category.name, category.name) for category in Category.objects.all().order_by('name')]
    all_glasses = [(glass.name, glass.name) for glass in Glass.objects.all().order_by('name')]
    all_ingredients = [(ingr.name, ingr.name) for ingr in Ingredient.objects.all().order_by('name')]
        
    name = forms.CharField(label="New drink name")
    non_alcoholic = forms.BooleanField(label="Non-alcoholic", required=False)
    category = forms.ChoiceField(label="Category", choices=all_categories, initial="Unspecified", required=True)
    glass = forms.ChoiceField(label="Glass", choices=all_glasses, initial="Unspecified", required=True)
    ingredients = forms.MultipleChoiceField(
        label = "Ingredients",
        required=True,
        widget= forms.SelectMultiple(attrs={'class': 'multiselect-dropdown'}),
        choices=all_ingredients,
    )
    instructions = forms.CharField(label="Description", max_length=3000, widget=forms.Textarea)
    image_url = forms.URLField(label="Image URL (optional)", required=False)
    