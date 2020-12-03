from django.urls import path
from . import views

urlpatterns = [

    path('recipes', views.get_recipes, name='get_recipes'),
    path('add', views.add_recipe, name='add_recipe'),
    path('details/<int:recipe_id>', views.recipe_details, name='recipe_details'),
    path('edit/<int:recipe_id>', views.edit_recipe, name='edit_recipe'),

]

app_name = 'cookbook'
