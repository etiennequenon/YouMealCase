from rest_framework import serializers
from .models import Nutrient, Ingredient, RecipeIngredient, Recipe

class NutrientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrient
        fields = ['id', 'name', 'amount', 'unit']

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if 'id' in data:
            internal_value['id'] = data['id']
        return internal_value

class IngredientSerializer(serializers.ModelSerializer):
    nutrient_information = NutrientSerializer(many=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'nutrient_information', 'allergen_information']

    def create(self, validated_data):
        nutrients_data = validated_data.pop('nutrient_information')
        ingredient = Ingredient.objects.create(**validated_data)
        for nutrient_data in nutrients_data:
            nutrient_id = nutrient_data.get('id')
            if nutrient_id:
                nutrient = Nutrient.objects.get(pk=nutrient_id)
                for attr, value in nutrient_data.items():
                    setattr(nutrient, attr, value)
                nutrient.save()
            else:
                nutrient = Nutrient.objects.create(**nutrient_data)
            ingredient.nutrient_information.add(nutrient)
        return ingredient

    def update(self, instance, validated_data):
        nutrients_data = validated_data.pop('nutrient_information')
        instance.name = validated_data.get('name', instance.name)
        instance.allergen_information = validated_data.get('allergen_information', instance.allergen_information)
        instance.save()

        # Update nutrients
        keep_nutrients = []
        for nutrient_data in nutrients_data:
            nutrient_id = nutrient_data.get('id')
            if nutrient_id:
                nutrient = Nutrient.objects.get(pk=nutrient_id)
                for attr, value in nutrient_data.items():
                    setattr(nutrient, attr, value)
                nutrient.save()
                keep_nutrients.append(nutrient.id)
            else:
                nutrient = Nutrient.objects.create(**nutrient_data)
                keep_nutrients.append(nutrient.id)

        # Remove old nutrients that are not in keep_nutrients
        instance.nutrient_information.set(Nutrient.objects.filter(id__in=keep_nutrients))

        return instance
    
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if 'id' in data:
            internal_value['id'] = data['id']
        return internal_value

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'quantity']

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient')
        ingredient_id = ingredient_data.get('id')
        if ingredient_id:
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            IngredientSerializer().update(ingredient, validated_data=ingredient_data)
        else:
            ingredient = IngredientSerializer().create(validated_data=ingredient_data)
        recipe_ingredient = RecipeIngredient.objects.create(ingredient=ingredient, **validated_data)
        return recipe_ingredient

    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredient')
        ingredient_id = ingredient_data.get('id')
        if ingredient_id:
            ingredient = Ingredient.objects.get(pk=ingredient_id)
            IngredientSerializer().update(ingredient, validated_data=ingredient_data)
        else:
            ingredient = IngredientSerializer().create(validated_data=ingredient_data)
        
        instance.ingredient = ingredient
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()

        return instance
    
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if 'id' in data:
            internal_value['id'] = data['id']
        return internal_value

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            if ingredient_id:
                ingredient = RecipeIngredient.objects.get(pk=ingredient_id)
                RecipeIngredientSerializer().update(ingredient, validated_data=ingredient_data)
            else:
                ingredient = RecipeIngredientSerializer().create(validated_data=ingredient_data)
            recipe.ingredients.add(ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Update ingredients
        keep_ingredients = []
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            if ingredient_id:
                ingredient = RecipeIngredient.objects.get(pk=ingredient_id)
                RecipeIngredientSerializer().update(ingredient, validated_data=ingredient_data)
                keep_ingredients.append(ingredient.id)
            else:
                ingredient = RecipeIngredientSerializer().create(validated_data=ingredient_data)
                keep_ingredients.append(ingredient.id)

        # Remove old ingredients that are not in keep_ingredients
        instance.ingredients.set(RecipeIngredient.objects.filter(id__in=keep_ingredients))

        return instance
    
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if 'id' in data:
            internal_value['id'] = data['id']
        return internal_value
