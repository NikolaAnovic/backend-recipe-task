from rest_framework import generics, filters, mixins
from rest_framework.permissions import IsAuthenticated
from .serializers import IngredientsSerializer, RecipesSerializer, CreateRecipesSerializer, RatingSerializer
from .models import Ingredient, RecipeRating, Recipe
from .paginators import CustomPagination
from django.db.models import Count

class IngredientsView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticated]

class CreateRecipesView(generics.CreateAPIView):
    queryset = Recipe.objects.select_related("recipe_author").prefetch_related("ingredient").all()
    serializer_class = CreateRecipesSerializer
    permission_classes = [IsAuthenticated]

class ListAllRecipesView(generics.ListAPIView):
    queryset = Recipe.objects.prefetch_related("ingredient").all()
    serializer_class = RecipesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "text", "ingredient__name"]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

class ListOwnRecipesView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Recipe.objects.prefetch_related("ingredient").all()
    serializer_class = RecipesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Recipe.objects.filter(recipe_author=self.request.user.id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class RecipeRatingView(generics.CreateAPIView):
    queryset = RecipeRating.objects.select_related("user").all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

class MostUsedIngredientsView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ingredient.objects.all().annotate(top_5_used_ingredients=Count("ingredients")).order_by("-top_5_used_ingredients")[:5]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
