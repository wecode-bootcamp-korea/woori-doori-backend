from django.urls import path
from .views import NewsView

urlpatterns = [
    path('/<int:nums>',NewsView.as_view()),
]

