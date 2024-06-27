from rest_framework import serializers
from .models import Ingredient, Nutrient, Recipe

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['id', 'name', 'amount', 'unit']

class IngredientSerializer(serializers.ModelSerializer):
    nutrient_information = NutrientSerializer(many=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'nutrient_information']

    def create(self, validated_data: dict) -> Ingredient:
        nutrients_data = validated_data.pop('nutrient_information')
        ingredient = Ingredient.objects.create(**validated_data)
        for nutrient_data in nutrients_data:
            nutrient, created = Nutrient.objects.get_or_create(**nutrient_data)
            ingredient.nutrient_information.add(nutrient)
        return ingredient

    def update(self, instance: Ingredient, validated_data: dict) -> Ingredient:
        nutrients_data = validated_data.pop('nutrient_information')
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        instance.nutrient_information.clear()
        for nutrient_data in nutrients_data:
            nutrient, created = Nutrient.objects.get_or_create(**nutrient_data)
            instance.nutrient_information.add(nutrient)

        return instance

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'ingredients']

    def create(self, validated_data: dict) -> Recipe:
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            nutrients_data = ingredient_data.pop('nutrient_information')
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_data['name'])
            for nutrient_data in nutrients_data:
                nutrient, created = Nutrient.objects.get_or_create(**nutrient_data)
                ingredient.nutrient_information.add(nutrient)
            recipe.ingredients.add(ingredient)
        return recipe

    def update(self, instance: Recipe, validated_data: dict) -> Recipe:
        ingredients_data = validated_data.pop('ingredients')
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        instance.ingredients.clear()
        for ingredient_data in ingredients_data:
            nutrients_data = ingredient_data.pop('nutrient_information')
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient_data['name'])
            ingredient.nutrient_information.clear()
            for nutrient_data in nutrients_data:
                nutrient, created = Nutrient.objects.get_or_create(**nutrient_data)
                ingredient.nutrient_information.add(nutrient)
            instance.ingredients.add(ingredient)

        return instance