from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)


class Ingredient(models.Model):
    name = models.CharField(max_length=50)


class IngredientSet(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.ManyToManyField(Ingredient, through='Quantity')


class Quantity(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE)
    set = models.ForeignKey(IngredientSet,
                            on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50, blank=True)
    unit = models.CharField(max_length=50, blank=True)


class Recipe(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    ingredients = models.ManyToManyField(IngredientSet)
    date = models.DateField(auto_now_add=True)
    website = models.CharField(max_length=200)
    picture = models.ImageField(blank=True, upload_to='images/')


class Procedure(models.Model):
    name = models.CharField(max_length=50)
    procedure = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
