from django.db import models


# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50, blank=True)
    time = models.CharField(max_length=50, blank=True)
    portions = models.CharField(max_length=50, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    ingredients = models.ManyToManyField(Ingredient)
    date = models.DateField(auto_now_add=True)
    website = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.name

    def get_json(self):
        json = {}
        for item in Recipe._meta.fields:
            # if item.name == "picture":
            #     json["picture"] = self.picture.name
            #     continue
            json[item.name] = getattr(self, item.name)

        ingredients = Ingredient.objects.filter(recipe=self)
        quantities = Quantity.objects.filter(recipe_id=json["id"])
        groups = {item.set for item in quantities}
        categories = self.categories.values_list().order_by("name")
        if categories.exists():
            json["categories"] = [category[1] for category in categories]

        json["ingredients"] = {}
        for group in groups:
            values = quantities.filter(set=group)
            keys = [ingredients.get(quantity=value) for value in values]
            json["ingredients"][group] = {key.name: value.quantity for key, value in zip(keys, values)}
        procedures = Procedure.objects.filter(recipe=self)
        json["recipe"] = {procedure.name: procedure.procedure for procedure in procedures}
        return json

    def get_absolute_url(self):
        return reverse('recipes:show_recipe', args=[self.id])


class Quantity(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)
    set = models.CharField(max_length=100, blank=True)
    quantity = models.CharField(max_length=100, blank=True)


class Procedure(models.Model):
    name = models.CharField(max_length=50)
    procedure = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.recipe, self.name)
