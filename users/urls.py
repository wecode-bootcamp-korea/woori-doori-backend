from django.urls import path
from .views import *


urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/signin', SigninView.as_view()),
    path('/google-auth', GoogleAuthView.as_view()),
    path('/kakao-auth', KakaoAuthView.as_view()),
]
