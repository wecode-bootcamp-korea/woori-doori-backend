from django.http import JsonResponse
from .models import *
from WooriDooriBackEnd import settings
import jwt


def user_auth_deco(func):
    def wrapper(self, request, *args, **kwargs):
        
        access_token = request.headers["Authorization"]
        algorithm = 'HS256'

        try:
            decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithm)
        except jwt.DecodeError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status = 401)
        else:
            if User.objects.filter(id = decoded_token["user_pk"]).exists():
                request.user_info = User.objects.get(id = decoded_token["user_pk"])
                return func(self, request, *args, **kwargs)
            else:
                return JsonResponse({"message":"INVALID_USER"}, status = 401)
            
        return wrapper
