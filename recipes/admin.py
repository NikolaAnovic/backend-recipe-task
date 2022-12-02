from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeRating

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeRating)