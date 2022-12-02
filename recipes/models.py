from django.db import models
from django.db.models import Avg
from user.models import User

RATING_CHOICE = [
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5'),
               ]

class Ingredient(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name    

class Recipe(models.Model):
    recipe_author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    text = models.TextField(max_length=300)
    ingredient = models.ManyToManyField(Ingredient, related_name='ingredients')

    @property
    def avg_rating(id):
        average_rating = RecipeRating.objects.filter(recipe=id).aggregate(Avg("rating"))['rating__avg']
        return average_rating

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class RecipeRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICE, null=True)
    
    def __str__(self):
        return self.recipe.name