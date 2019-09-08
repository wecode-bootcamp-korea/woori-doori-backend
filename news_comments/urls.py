from django.urls import path
from .views import NewsCommentsView, UpdateCommentsView

urlpatterns = [
	path('/<int:news_id>', NewsCommentsView.as_view()),
	path('/<int:news_id>/update', UpdateCommentsView.as_view()),
]
