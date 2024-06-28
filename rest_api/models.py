from django.db import models

class Nutrient(models.Model):
    name = models.CharField(max_length=50)
    amount = models.FloatField()
    unit = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}: {self.amount} {self.unit}'

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    nutrient_information = models.ManyToManyField(Nutrient)
    allergen_information = models.TextField(max_length=2048, null=True)

    def __str__(self):
        return self.name
    
class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.quantity} {self.ingredient}"

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(RecipeIngredient)

    def __str__(self):
        return self.name