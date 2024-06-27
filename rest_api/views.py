from rest_framework import generics, permissions
from .models import Ingredient, Nutrient, Recipe
from .serializers import IngredientSerializer, NutrientSerializer, RecipeSerializer

class IngredientList(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

class IngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]

class NutrientList(generics.ListCreateAPIView):
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer
    permission_classes = [permissions.IsAuthenticated]

class NutrientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nutrient.objects.all()
    serializer_class = NutrientSerializer
    permission_classes = [permissions.IsAuthenticated]

class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
