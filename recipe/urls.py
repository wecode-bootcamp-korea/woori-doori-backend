from django.urls import path
from .views import CategoryView, RecipeView, Comments

urlpatterns = [
    path('category', CategoryView.as_view()),
    path('recipes', RecipeView.as_view()),
    path('comments', Comments.as_view())
]
