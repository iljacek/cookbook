from django.core.exceptions import ValidationError
from django.forms import ModelForm, widgets, IntegerField
from django import forms
from recipes.models import Recipe, Procedure, Category, Ingredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('date', 'author', 'ingredients', 'categories')


class RecipeURLForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['website']

