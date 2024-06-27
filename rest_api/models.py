from django.db import models

class Nutrient(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    unit = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}: {self.amount} {self.unit}'

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    nutrient_information = models.ManyToManyField(Nutrient)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient)