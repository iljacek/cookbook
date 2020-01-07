import json

import requests
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader

import recipes.URL_parser as URL_parser

# Create your views here.
from recipes.forms import RecipeForm, RecipeURLForm
from recipes.models import Recipe, Procedure, Ingredient, Quantity, Category


# def welcome(request):
#     my_recipes = Recipe.objects.filter(author=request.user)
#     return render(request, "Cookbook/welcome.html", {'my_recipes': my_recipes})


@login_required
def home(request):
    my_recipes = Recipe.objects.filter(author=request.user)
    categories = Category.objects.all()
    context = {"my_recipes": my_recipes, "categories": categories}

    return render(request, "Cookbook/home.html", context)


@login_required
def search(request):
  query = request.POST['name']
  t = loader.get_template('Cookbook/home.html')
  c ={'query': query}
  return HttpResponse(t.render(c))


def autocompleteModel(request, field):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        if field == "recipe":
            search_qs = Recipe.objects.filter(name__icontains=q)
        else:
            search_qs = Ingredient.objects.filter(name__icontains=q)
        results = []
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def search_results(request):
    if request.method == 'POST':
        if request.POST["type"] == 'ingredient':
            my_recipes = Recipe.objects.filter(author=request.user, ingredients__name__contains=request.POST["name"])
        elif request.POST["type"] == 'category':
            my_recipes = Recipe.objects.filter(author=request.user, categories__name=request.POST["name"])
        else:
            my_recipes = Recipe.objects.filter(author=request.user, name__contains=request.POST['name'])
        my_recipes = set(my_recipes)
    else:
        my_recipes = Recipe.objects.filter(author=request.user)
    categories = Category.objects.all().order_by("name")
    context = {"my_recipes": my_recipes, "categories": categories}
    return render(request, "Cookbook/home.html", context)


@login_required
def show_recipe(request, recipe):
    record = Recipe.objects.get(id=recipe)
    record = record.get_json()
    return render(request, 'recipes/show_recipe.html', record)


@login_required
def new_recipe(request):
    if request.method == "POST":
        recipe = Recipe()
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            complete_form = form.save(commit=False)
            complete_form.author = request.user.get_username()
            result = dict(form.data)
            complete_form.save()

            for ingredient, quantity, group in zip(result["ingredient"], result["quantity"], result["group"]):
                new_ingredient = Ingredient.objects.get_or_create(name=ingredient)
                complete_form.ingredients.add(new_ingredient[0].pk)
                Quantity.objects.get_or_create(ingredient=new_ingredient[0], recipe=complete_form, quantity=quantity, set=group)

            for step, text in zip(result["step"], result["text"]):
                Procedure.objects.get_or_create(recipe=complete_form, name=step, procedure=text)

            for category in result["category"]:
                new_category = Category.objects.get_or_create(name=category)
                complete_form.categories.add(new_category[0].pk)

            form.save_m2m()

            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, "recipes/dynamic_recipe.html", {'form': form})


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
                if key != "ingredients" and key != "recipe" and key != "image":
                    setattr(complete_form, key, value)
                elif key == "image":
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(requests.get(value).content)
                    img_temp.flush()

                    complete_form.picture.save(record.record["name"].replace(u' ', u'_')+".jpg", File(img_temp))
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
