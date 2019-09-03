from django.urls import path
from .views import NewsView

urlpatterns = [
    path('/<int:tag_nums>/<int:nums>',NewsView.as_view()),
]

