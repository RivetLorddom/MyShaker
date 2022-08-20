from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Category, Glass, Ingredient

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
        
    name = forms.CharField(label="New drink name")
    non_alcoholic = forms.BooleanField(label="Non-alcoholic", required=False)
    category = forms.ModelChoiceField(label="Category", queryset=Category.objects.all(), empty_label='Select the category', required=True)
    glass = forms.ModelChoiceField(label="Glass", queryset=Glass.objects.all(), empty_label='Select the glass', required=True)
    ingredients = forms.ModelMultipleChoiceField(
        label = "Ingredients",
        required=True,
        widget= forms.SelectMultiple(attrs={'class': 'multiselect'}),
        queryset=Ingredient.objects.all().order_by('name'),
    )
    
    instructions = forms.CharField(label="Instructions", max_length=3000, widget=forms.Textarea)
    image_url = forms.URLField(label="Image URL (optional)", required=False)
    