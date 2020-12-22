from django import forms
from django.forms import ModelForm
from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['image', 'title', 'ingredients', 'preparing']


class UrlRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('image', 'title', 'ingredients', 'preparing')