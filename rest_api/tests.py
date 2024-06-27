import base64
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Ingredient, Nutrient, Recipe
from django.urls import reverse
from django.contrib.auth.models import User


class BaseTestsWithBasicAuth(TestCase):
    """
    Class to inherit for the tests that requires Basic Auth.

    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a base64 encoded credentials string
        credentials = base64.b64encode(b'testuser:testpassword').decode('utf-8')
        self.client.credentials(HTTP_AUTHORIZATION='Basic ' + credentials)


class IngredientAPITestCase(BaseTestsWithBasicAuth):
    def setUp(self):
        super().setUp()
        self.nutrient1 = Nutrient.objects.create(name="Protein", amount=10, unit="g")
        self.nutrient2 = Nutrient.objects.create(name="Fat", amount=5, unit="g")
        self.ingredient_data = {
            "name": "Chicken Breast",
            "nutrient_information": [
                {"name": "Protein", "amount": 10, "unit": "g"},
                {"name": "Fat", "amount": 5, "unit": "g"}
            ]
        }
        self.ingredient = Ingredient.objects.create(name="Chicken Breast")
        self.ingredient.nutrient_information.set([self.nutrient1, self.nutrient2])

    def test_create_ingredient(self):
        response = self.client.post(reverse('ingredient-list'), self.ingredient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ingredient.objects.count(), 2)
        self.assertEqual(Nutrient.objects.count(), 2)  # Ensures no new Nutrients are created

    def test_get_ingredient(self):
        response = self.client.get(reverse('ingredient-detail', kwargs={'pk': self.ingredient.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.ingredient.name)

    def test_update_ingredient(self):
        update_data = {
            "name": "Updated Chicken Breast",
            "nutrient_information": [
                {"name": "Protein", "amount": 15, "unit": "g"},
                {"name": "Fat", "amount": 5, "unit": "g"}
            ]
        }
        response = self.client.put(reverse('ingredient-detail', kwargs={'pk': self.ingredient.id}), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ingredient.refresh_from_db()
        self.assertEqual(self.ingredient.name, "Updated Chicken Breast")
        self.assertEqual(self.ingredient.nutrient_information.get(name='Protein').amount, 15)
        self.assertEqual(self.ingredient.nutrient_information.get(name='Fat').amount, 5)

    def test_delete_ingredient(self):
        response = self.client.delete(reverse('ingredient-detail', kwargs={'pk': self.ingredient.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ingredient.objects.count(), 0)

class RecipeAPITestCase(BaseTestsWithBasicAuth):
    def setUp(self):
        super().setUp()
        self.nutrient1 = Nutrient.objects.create(name="Protein", amount=10, unit="g")
        self.nutrient2 = Nutrient.objects.create(name="Fat", amount=5, unit="g")
        self.ingredient1 = Ingredient.objects.create(name="Chicken Breast")
        self.ingredient1.nutrient_information.set([self.nutrient1, self.nutrient2])
        self.ingredient2 = Ingredient.objects.create(name="Olive Oil")
        self.ingredient2.nutrient_information.set([self.nutrient2])
        self.recipe_data = {
            "name": "Grilled Chicken",
            "ingredients": [
                {
                    "name": "Chicken Breast",
                    "nutrient_information": [
                        {"name": "Protein", "amount": 10, "unit": "g"},
                        {"name": "Fat", "amount": 5, "unit": "g"}
                    ]
                },
                {
                    "name": "Olive Oil",
                    "nutrient_information": [
                        {"name": "Fat", "amount": 5, "unit": "g"}
                    ]
                }
            ]
        }
        self.recipe = Recipe.objects.create(name="Grilled Chicken")
        self.recipe.ingredients.set([self.ingredient1, self.ingredient2])

    def test_create_recipe(self):
        response = self.client.post(reverse('recipe-list'), self.recipe_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(Ingredient.objects.count(), 2)  # Ensures no new Ingredients are created

    def test_get_recipe(self):
        response = self.client.get(reverse('recipe-detail', kwargs={'pk': self.recipe.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.recipe.name)

    def test_update_recipe(self):
        update_data = {
            "name": "Updated Grilled Chicken",
            "ingredients": [
                {
                    "name": "Chicken Breast",
                    "nutrient_information": [
                        {"name": "Protein", "amount": 20, "unit": "g"},
                        {"name": "Fat", "amount": 10, "unit": "g"}
                    ]
                },
                {
                    "name": "Olive Oil",
                    "nutrient_information": [
                        {"name": "Fat", "amount": 5, "unit": "g"}
                    ]
                }
            ]
        }
        response = self.client.put(reverse('recipe-detail', kwargs={'pk': self.recipe.id}), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, "Updated Grilled Chicken")
        self.assertEqual(self.recipe.ingredients.first().nutrient_information.first().amount, 20)

    def test_delete_recipe(self):
        response = self.client.delete(reverse('recipe-detail', kwargs={'pk': self.recipe.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)
