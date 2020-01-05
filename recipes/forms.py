from django.core.exceptions import ValidationError
from django.forms import ModelForm, widgets

from recipes.models import Recipe, Procedure, Category, Ingredient


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('date', 'author')

    # def __init__(self, *args, **kwargs):
    #     super(RecipeForm, self).__init__(*args, **kwargs)
    #     self.fields["categories"].widget = widgets.CheckboxSelectMultiple()
    #     self.fields["categories"].help_text = ""
    #     self.fields["categories"].queryset = Category.objects.all()
    #     self.fields["ingredients"].widget = widgets.CheckboxSelectMultiple()
    #     self.fields["ingredients"].help_text = ""
    #     self.fields["ingredients"].queryset = IngredientSet.objects.all()


class StepForm(ModelForm):
    class Meta:
        model = Procedure
        exclude = ('recipe',)


class RecipeURLForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['website']

    # def save(self, *args, **kwargs):
    #     if not commit:
    #         raise NotImplementedError("Can't create User and Userextended without database save")
    #     # recipe = super().save(*args, **kwargs)
    #     recipe = Recipe(name=self.cleaned_data['name'], website=self.cleaned_data['website'])
    #     user_profile.save()
    #     user_profile.rolle.add(self.cleaned_data['rolle'])
    #     user_profile.save()
    #     return user
