from django.shortcuts import render


def recipes(request):
    return render(request, 'cookbook/recipes.html')
