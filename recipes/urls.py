from django.urls import path
from .views import CreateRecipesView, IngredientsView, ListAllRecipesView, ListOwnRecipesView, RecipeRatingView, MostUsedIngredientsView

urlpatterns = [
    path("ingredients/", IngredientsView.as_view(), name="ingredients"),
    path("", ListAllRecipesView.as_view(), name="all_recipes"),
    path("user/", ListOwnRecipesView.as_view(), name="user_recipes"),
    path("create/", CreateRecipesView.as_view(), name="create_recipes"),
    path("rate/", RecipeRatingView.as_view(), name="rate"),
    path("top-5-ingredients/", MostUsedIngredientsView.as_view(), name="top_5_most_used_ingredients")
]