from django.urls import path
from . import views

urlpatterns = [

    path('recipes', views.get_recipes, name='get_recipes'),
    path('details/<int:recipe_id>', views.recipe_details, name='recipe_details')
]

app_name = 'cookbook'
