from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm


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
            form = RecipeForm(request.POST, request.FILES)
            new_recipe = form.save(commit=False)
            new_recipe.user = request.user
            new_recipe.save()
            return redirect('cookbook:recipe_details', recipe_id=new_recipe.id)
        except ValueError:
            return render(request, 'cookbook/new_recipe.html', {'form': form, 'error': error})


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

