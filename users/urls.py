from django.urls import path
from .views import *


urlpatterns = [
    path('/signup', SignUp.as_view()),
    path('/login', LogIn.as_view()), 
]
