import base64
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Ingredient, Nutrient, Recipe, RecipeIngredient
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

class NutrientTests(BaseTestsWithBasicAuth):
    def test_create_nutrient(self):
        url = reverse('nutrient-list')
        data = {'name': 'Carbohydrate', 'amount': 20, 'unit': 'g'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_get_nutrient(self):
        nutrient = Nutrient.objects.create(name= 'Fat', amount= 10, unit= 'g')
        url = reverse('nutrient-detail', args=[nutrient.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.data['name'], nutrient.name)

class IngredientTests(BaseTestsWithBasicAuth):
    def setUp(self):
        super().setUp()
        self.nutrient = Nutrient.objects.create(name='Protein', amount=10, unit='g')
        self.ingredient = Ingredient.objects.create(name='Chicken', allergen_information="NSFW")
        self.ingredient.nutrient_information.add(self.nutrient)

    def test_create_ingredient(self):
        url = reverse('ingredient-list')
        data = {'name': 'Beef', 'nutrient_information': [{'name': 'Protein', 'amount': 10, 'unit': 'g'}], 'allergen_information': 'Not Safe For Work'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

    def test_get_ingredient(self):
        url = reverse('ingredient-detail', args=[self.ingredient.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.data['name'], 'Chicken')

class RecipeTests(BaseTestsWithBasicAuth):
    def setUp(self):
        super().setUp()
        self.nutrient1 = Nutrient.objects.create(name='Protein', amount=10, unit='g')
        self.ingredient1 = Ingredient.objects.create(name='Vegetables')
        self.ingredient1.nutrient_information.add(self.nutrient1)
        self.nutrient2  = Nutrient.objects.create(name='Protein', amount=10, unit='g')
        self.ingredient2 = Ingredient.objects.create(name='Chicken')
        self.ingredient2.nutrient_information.add(self.nutrient2)
        self.recipe_ingredient1 = RecipeIngredient.objects.create(ingredient=self.ingredient1, quantity=2)
        self.recipe_ingredient2 = RecipeIngredient.objects.create(ingredient=self.ingredient2, quantity=10)
        self.data = {
                    'name': 'Cooked beef',
                    'ingredients': [
                        {
                            'id': self.recipe_ingredient2.id,
                            'ingredient': {
                                'name': 'Chicken',
                                'nutrient_information': [
                                    {
                                        'id': self.nutrient2.id,
                                        'name': 'Protein',
                                        'amount': 10,
                                        'unit': 'g'
                                    }
                                ],
                                'allergen_information': 'NSFW',
                                'id': self.ingredient2.id
                            },
                            'quantity': 10.0
                        },
                        {
                            'id': self.recipe_ingredient1.id,
                            'ingredient': {
                                'name': 'Vegetables',
                                'nutrient_information': [
                                    {
                                        'id': self.nutrient1.id,
                                        'name': 'Protein',
                                        'amount': 10,
                                        'unit': 'g'
                                    }
                                ],
                                'allergen_information': 'NSFW',
                                'id': self.ingredient1.id
                            },
                            'quantity': 10.0
                        }
                    ]
                }

    def test_create_recipe(self):
        # Test with already generated nutrient and ingredient
        url = reverse('recipe-list')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())
        json_response = response.json()
        json_response.pop('id') # pop the id key as it will be created.
        self.assertEqual(json_response, self.data, json_response)
        # Now test the a complete creation of all items.
        scratch_recipe = self.data.copy()
        for i in range(len(scratch_recipe['ingredients'])):
            scratch_recipe['ingredients'][i].pop('id')
            scratch_recipe['ingredients'][i]['ingredient'].pop('id')
            scratch_recipe['ingredients'][i]['ingredient']['nutrient_information'][0].pop('id')
        response = self.client.post(url, scratch_recipe, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(Ingredient.objects.count(), 4)
        self.assertEqual(Nutrient.objects.count(), 4)

    def test_get_recipe(self):
        url = reverse('recipe-list')
        created_recipe = self.client.post(url, self.data, format='json').json()
        url = reverse('recipe-detail', args=[created_recipe.get('id')])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.json())
        self.assertEqual(response.json(), created_recipe)

    def test_update_recipe(self):
        url = reverse('recipe-list')
        created_recipe = self.client.post(url, self.data, format='json').json()
        url = reverse('recipe-detail', args=[created_recipe.get('id')])
        created_recipe['ingredients'][0]['ingredient']['allergen_information'] = 'NotSafeForWork'
        created_recipe['ingredients'][0]['ingredient']['nutrient_information'][0]['amount'] = 20
        response = self.client.put(url, created_recipe, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        # Check the HTTP response.
        self.assertEqual(response.json(), created_recipe, f'Got {response.json()}\n\n Expected {created_recipe}') 
        # Check the Database values.
        self.assertEqual(Ingredient.objects.get(pk=created_recipe['ingredients'][0]['ingredient'].get('id')).allergen_information, 'NotSafeForWork')
        self.assertEqual(Nutrient.objects.get(pk=created_recipe['ingredients'][0]['ingredient']['nutrient_information'][0].get('id')).amount, 20)
