from django.urls import path
from .views import CategoryView, RecipeView

urlpatterns = [
    path('category', CategoryView.as_view()),
    path('recipes', RecipeView.as_view()), 
]
