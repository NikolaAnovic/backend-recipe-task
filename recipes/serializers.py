from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from recipes.models import Ingredient, Recipe, RecipeRating

class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ("name",)

class CreateRecipesSerializer(serializers.ModelSerializer):
    recipe_author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ("recipe_author", "name", "text", "ingredient")

class RecipesSerializer(serializers.ModelSerializer):
    avg_rating = serializers.ReadOnlyField()
    ingredient = IngredientsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ("recipe_author", "name", "text", "ingredient", "avg_rating")

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RecipeRating 
        fields = ("user", "recipe", "rating")

    def create(self, validated_data):
        recipe = validated_data["recipe"]
        if recipe.recipe_author == validated_data["user"]:
            raise ValidationError("You can not rate your own recipe!")
        if RecipeRating.objects.filter(user=validated_data["user"], recipe=validated_data["recipe"]).exists():
            raise ValidationError("You already voted once!")
        return RecipeRating.objects.create(**validated_data)