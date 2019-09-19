from django.urls import path
from .views      import CategoryView, RecipeView

urlpatterns = [
    path('/category', CategoryView.as_view()),
    path('/recipes', RecipeListView.as_view()), 
    path('/recipe/<int:recipe_id>', RecipeListView.as_view())
]
