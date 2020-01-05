import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader

import recipes.URL_parser as URL_parser

# Create your views here.
from recipes.forms import RecipeForm, StepForm, RecipeURLForm
from recipes.models import Recipe, Procedure, Ingredient, Quantity


@login_required
def home(request):
    my_recipes = Recipe.objects.filter(author=request.user)
    return render(request, "Cookbook/home.html", {'my_recipes': my_recipes})


@login_required
def get_from_url(request, site):
    record = Recipe.objects.get(id=55)
    record = record.get_json()
    return render(request, 'recipes/show_recipe.html', record)


@login_required
def new_recipe(request):
    if request.method == "POST":
        recipe = Recipe()
        form = RecipeForm(instance=recipe, data=request.POST)
        if form.is_valid():
            complete_form = form.save(commit=False)
            complete_form.author = request.user.get_username()
            complete_form.save()
            return redirect('recipes:new_step', recipe=recipe.id)
    else:
        form = RecipeForm()
    return render(request, "recipes/recipe_form.html", {'form': form})


@login_required
def new_step(request, recipe):
    if request.method == "POST":
        procedure = Procedure()
        form = StepForm(instance=procedure, data=request.POST)
        if form.is_valid():
            complete_form = form.save(commit=False)
            complete_form.recipe = Recipe.objects.get(id=recipe)
            complete_form.save()

            if 'add_step' in request.POST:
                return redirect('recipes:new_step', recipe=recipe)
            elif 'finish' in request.POST:
                return redirect('home')
    else:
        form = StepForm()
    return render(request, "recipes/procedure_form.html", {'form': form, 'recipe': recipe})


@login_required
def new_from_url(request):
    if request.method == "POST":
        recipe = Recipe()
        form = RecipeURLForm(instance=recipe, data=request.POST)
        if form.is_valid():
            complete_form = form.save(commit=False)
            if complete_form.website.find("apetitonline") >= 0:
                record = URL_parser.ApetitRecord(complete_form.website)
            elif complete_form.website.find("varecha") >= 0:
                record = URL_parser.VarechaRecord(complete_form.website)
            else:
                record = URL_parser.DobruchutRecord(complete_form.website)
            complete_form.author = request.user.get_username()
            record.scrape_data()

            for key, value in record.record.items():
                if key != "ingredients" and key != "recipe":
                    setattr(complete_form, key, value)
            complete_form.save()

            # new_recipe = Recipe(website=recipe.website, name=record.record["name"])
            for group, items in record.record["ingredients"].items():
                for item, quantity in items.items():
                    new_ingredient = Ingredient.objects.get_or_create(name=item)
                    complete_form.ingredients.add(new_ingredient[0].pk)
                    Quantity.objects.get_or_create(ingredient=new_ingredient[0], recipe=complete_form, quantity=quantity, set=group)

            for name, step in record.record["recipe"].items():
                Procedure.objects.get_or_create(recipe=complete_form, name=name, procedure=step)

            form.save_m2m()
            return redirect('home')
    else:
        form = RecipeURLForm()
    return render(request, "recipes/url_form.html", {'form': form})
