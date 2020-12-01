from django.shortcuts import render, get_object_or_404
from .models import Recipe


def get_recipes(request):
    my_recipes = Recipe.objects.filter(user=request.user).order_by('-date_added')
    return render(request, 'cookbook/recipes.html', {'my_recipes': my_recipes})


def recipe_details(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'cookbook/recipe.html', {'recipe': recipe})
