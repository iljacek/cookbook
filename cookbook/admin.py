from django.contrib import admin
from cookbook.models import Ingredient, IngredientSet, Procedure, Category, Recipe, Quantity
# Register your models here.


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(IngredientSet)
class IngredientSetAdmin(admin.ModelAdmin):
    list_display = ('name', )       # 'ingredients',


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'procedure', 'recipe',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'website', 'picture',)       # 'categories', 'ingredients',


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'set', 'quantity', 'unit',)
