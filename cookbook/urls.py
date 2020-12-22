from django.urls import path
from . import views

urlpatterns = [

    path('recipes', views.get_recipes, name='get_recipes'),
    path('details/<int:recipe_id>', views.recipe_details, name='recipe_details'),
    path('add', views.add_recipe, name='add_recipe'),
    path('add_link', views.add_recipe_link, name='add_recipe_link'),
    path('add_recipe_from_url', views.add_recipe_from_url, name='add_recipe_from_url'),
    path('edit/<int:recipe_id>', views.edit_recipe, name='edit_recipe'),
    path('delete/<int:recipe_id>', views.delete_recipe, name='delete_recipe'),

]

app_name = 'cookbook'
