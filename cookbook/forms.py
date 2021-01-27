from django.forms import ModelForm, ValidationError
from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['image', 'title', 'ingredients', 'preparing']



