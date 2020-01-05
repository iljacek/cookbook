from django.core.exceptions import ValidationError
from django.forms import ModelForm, widgets, IntegerField
from django import forms
from recipes.models import Recipe, Procedure, Category, Ingredient


class RecipeForm(ModelForm):
    group = forms.CharField(required=False)
    ingredient = forms.CharField(required=False)
    amount = forms.CharField(required=False)

    class Meta:
        model = Recipe
        exclude = ('date', 'author')

    def save(self, commit=True):
        # do something with self.cleaned_data['temp_id']
        return super(RecipeForm, self).save(commit=commit)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     ingredients = Ingredient.objects.filter(
    #         recipe=self.instance
    #     )
    #     for i in range(len(ingredients) + 1):
    #         field_name = 'ingredient_%s' % (i,)
    #         self.fields[field_name] = forms.CharField(required=False)
    #         try:
    #             self.initial[field_name] = ingredients[i].ingredient
    #         except IndexError:
    #             self.initial[field_name] = ""
    #     # create an extra blank field
    #     field_name = 'ingredient_%s' % (i + 1,)
    #     self.fields[field_name] = forms.CharField(required=False)
    #
    # def clean(self):
    #     ingredients = set()
    #     i = 0
    #     field_name = 'ingredient_%s' % (i,)
    #     while self.cleaned_data.get(field_name):
    #        ingredient = self.cleaned_data[field_name]
    #        if ingredient in ingredients:
    #            self.add_error(field_name, 'Duplicate')
    #        else:
    #            ingredients.add(ingredient)
    #        i += 1
    #        field_name = 'ingredient_%s' % (i,)
    #     self.cleaned_data["ingredients"] = ingredients
    #
    # def save(self):
    #     recipe = self.instance
    #     recipe.name = self.cleaned_data["name"]
    #
    #     recipe.ingredients_set.all().delete()
    #     for ingredient in self.cleaned_data["ingredients"]:
    #         Ingredient.objects.create(
    #             recipe=recipe,
    #             ingredient=ingredient,
    #         )
    #
    # def get_interest_fields(self):
    #     for field_name in self.fields:
    #         if field_name.startswith("ingredient_"):
    #             yield self[field_name]


class StepForm(ModelForm):
    class Meta:
        model = Procedure
        exclude = ('recipe',)


class RecipeURLForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['website']

