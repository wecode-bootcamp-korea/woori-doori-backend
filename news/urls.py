from django.urls import path
from .views import NewsView, TagView, DetailNewsView

urlpatterns = [
    path('',NewsView.as_view()),
	path('/<int:news_id>',DetailNewsView.as_view()),
	path('/tags',TagView.as_view()),
]

