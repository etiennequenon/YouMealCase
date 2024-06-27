from django.urls import path
from .views import IngredientList, IngredientDetail, NutrientList, NutrientDetail, RecipeList, RecipeDetail

urlpatterns = [
    path('ingredients/', IngredientList.as_view(), name='ingredient-list'),
    path('ingredients/<int:pk>/', IngredientDetail.as_view(), name='ingredient-detail'),
    path('nutrients/', NutrientList.as_view(), name='nutrient-list'),
    path('nutrients/<int:pk>/', NutrientDetail.as_view(), name='nutrient-detail'),
    path('recipes/', RecipeList.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetail.as_view(), name='recipe-detail'),
]
