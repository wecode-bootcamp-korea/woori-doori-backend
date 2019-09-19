from django.urls import path
from .views import NewsView, TagView, DetailNewsView

urlpatterns = [
    path('',NewsListView.as_view()),
	path('/<int:news_id>',NewsView.as_view()),
	path('/tags',TagView.as_view()),
]

