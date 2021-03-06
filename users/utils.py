from WooriDooriBackEnd import settings
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import User
import jwt
import json

def validate_login(func):
	def wrapper(self, request, *args, **kwargs):
		if 'Authorization' not in request.headers:
			return JsonResponse({'message':'NOT_ALLOWED'}, status = 401)
		
		access_token = request.headers['Authorization']

		try:
			user_data = jwt.decode(access_token, settings.SECRET_KEY, algorithm='HS256')
			user = User.objects.get(id = user_data['id'])
			request.user = user
		except jwt.DecodeError:
			return JsonResponse({'message':'INVALID_TOKEN'}, status = 401)
		except ObjectDoesNotExist:
			return JsonResponse({'message':'USER_NOT_EXISTS'}, status = 401)
		return func(self, request, *args, **kwargs)

	return wrapper
