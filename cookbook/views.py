import os

from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm, UrlRecipeForm
import requests
from bs4 import BeautifulSoup
import urllib.request
from django.core.files import File


@login_required
def get_recipes(request):
    query = request.GET.get('search')

    if query:
        results = Recipe.objects.filter(user=request.user, title__contains=query)
    else:
        results = Recipe.objects.filter(user=request.user).order_by('-date_added')
    return render(request, 'cookbook/recipes.html', {'results': results, 'query': query})


@login_required
def add_recipe(request):
    form = RecipeForm()
    error = "Bad data passed in. Try again."

    if request.method == 'GET':
        return render(request, 'cookbook/new_recipe.html', {'form': form})
    else:
        try:
            print(request.FILES)
            form = RecipeForm(request.POST, request.FILES)
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user
            print(new_recipe.image)
            new_recipe.save()
            return redirect('cookbook:recipe_details', recipe_id=new_recipe.id)
        except ValueError:
            return render(request, 'cookbook/new_recipe.html', {'form': form, 'error': error})


@login_required
def add_recipe_link(request):
    if request.method == 'GET':
        return render(request, 'cookbook/new_link.html')
    else:
        website_link = request.POST.get('web_link')
        url = website_link
        page = requests.get(url)
        soupe = BeautifulSoup(page.content, 'html.parser')

        title = soupe.find(class_='przepis page-header').get_text()

        ingredients = soupe.find(class_='field-name-field-skladniki')
        ul = ingredients.find_all('ul')
        items = []
        for li in ul:
            items.append(li.get_text())

        preparing = soupe.find(class_='field-name-field-przygotowanie')
        ul = preparing.find_all('ul')
        actions = []
        for li in ul:
            actions.append(li.get_text())

        image = soupe.find(class_='img-responsive')
        image_url = image['src']
        img_name = os.path.basename(image_url)
        print(img_name)
        image_path = os.path.join('media/images/', img_name)
        print(image_path)
        photo = urllib.request.urlretrieve(image_url, image_path)
        print(photo)

        recipe = Recipe()

        recipe.preparing = "".join(actions)
        recipe.ingredients = "".join(items)
        recipe.title = title
        recipe.image = photo[0]

        form = UrlRecipeForm(instance=recipe)

        return render(request, 'cookbook/new_recipe_from_url.html',
                      {'form': form})


@login_required
def add_recipe_from_url(request):
    form = UrlRecipeForm()
    error = "Bad data passed in. Try again."

    if request.method == 'GET':
        return render(request, 'cookbook/new_recipe_from_url.html', {'form': form})
    else:
        try:
            print(request.FILES)
            form = UrlRecipeForm(request.POST, request.FILES)
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user
            new_recipe.save()
            return redirect('cookbook:recipe_details', recipe_id=new_recipe.id)
        except ValueError:
            return render(request, 'cookbook/new_recipe_from_url.html', {'form': form, 'error': error})


@login_required
def recipe_details(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id, user=request.user)
    return render(request, 'cookbook/recipe.html', {'recipe': recipe})


@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id, user=request.user)

    if request.method == 'GET':
        form = RecipeForm(instance=recipe)
        return render(request, 'cookbook/edit_recipe.html', {'recipe': recipe, 'form': form})
    else:
        try:

            print(request.FILES, recipe.image)
            form = RecipeForm(request.POST, request.FILES, instance=recipe)
            form.save()
            return redirect('cookbook:recipe_details', recipe_id=recipe.id)
        except ValueError:
            render(request, 'cookbook/edit_recipe.html', {'recipe': recipe, 'form': form, 'error': "Bad info :/"})


@login_required
def delete_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id, user=request.user)

    if request.method == 'POST':
        recipe.delete()
        return redirect('cookbook:get_recipes')
