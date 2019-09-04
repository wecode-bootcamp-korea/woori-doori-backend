from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, SocialPlatform
from WooriDooriBackEnd import settings
import bcrypt
import json
import jwt
import datetime
import requests
import pdb


class SignupView(View):
    FIELDS = {
        "user_id" : "FILL_USERID",
        "name" : "FILL_USERNAME",
        "password" : "FILL_USER_PASSWORD",
        "email" : "FILL_USER_EMAIL"
    }

    def _validate_user_input(self, data):
        for field, message in self.FIELDS.items():
            if data.get(field) is None or len(data[field]) == 0:
                return {"message" : message}

    def post(self, request):
        user_data = json.loads(request.body)
        field_validation = self._validate_user_input(user_data)

        if field_validation is not None:
            return JsonResponse(field_validation, status = 401)

        if User.objects.filter(user_id = user_data['user_id']).exists():
            return JsonResponse({'message' : 'USER_EXISTS'}, status = 409)

        encrypted_pw = bcrypt.hashpw(bytes(user_data['password'], 'utf-8'), bcrypt.gensalt())

        User(
                user_id  = user_data['user_id'],
                name     = user_data['name'],
                password = encrypted_pw.decode('utf-8'),
                email    = user_data['email'],
                photo    = user_data.get('photo', ""),
                profile  = user_data.get('profile', ""),
                ).save()

        return HttpResponse(status = 200)

class SigninView(View):
    def post(self, request):
        user_data = json.loads(request.body)

        if user_data.get('user_id') is None or len(user_data['user_id']) == 0:
            return JsonResponse({'message' : 'FILL_ID'}, status = 401)

        if user_data.get('password') is None or len(user_data['password']) == 0:
            return JsonResponse({'message' : 'FILL_PASSWORD'}, status = 401)

        try:
            user_info = User.objects.get(user_id = user_data['user_id'])

        except ObjectDoesNotExist:
            return JsonResponse({'message' : 'USER_NOT_EXIST'}, status = 401)

        if bcrypt.checkpw(user_data['password'].encode('utf-8'), user_info.password.encode('utf-8')):
            payload = {
                'id': user_info.id,
                'exp': datetime.datetime.now() + datetime.timedelta(seconds = 60 * 60 * 24),
            }

            encoded_key = settings.SECRET_KEY
            algorithm = 'HS256'
            token = jwt.encode(payload, encoded_key, algorithm)
            return JsonResponse({'access_token' : token.decode('utf-8')}, safe = False, status = 200)
        else:
            return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 401)

class GoogleAuthView(View):
    def get(self, request):
        access_token = request.headers["Authorization"]
        url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
        response = requests.get(url+access_token)
        user = response.json()

        encoded_key = settings.SECRET_KEY
        algorithm = 'HS256'

        if User.objects.filter(social_user_id = user['sub']).exists():
            user_info = User.objects.get(social_user_id = user['sub'])
            payload = {
                'id' : user_info.id,
                'google_id' : user['sub'],
                'exp': datetime.datetime.now() + datetime.timedelta(seconds = 60 * 60 * 24),
                }
            token = jwt.encode(payload, encoded_key, algorithm)
            return JsonResponse({'access_token' : token.decode('UTF-8')}, status = 200)

        else:
            new_user_info = User(
                    social_user_id = user['sub'],
                    social = SocialPlatform.objects.get(platform = 'google')
                    )
            new_user_info.save()
            
            payload = {
                'id' : User.objects.get(social_user_id = user['sub']).id,
                'google_id' : user['sub'],
                'exp': datetime.datetime.now() + datetime.timedelta(seconds = 60 * 60 * 24),
                }
            token = jwt.encode(payload, encoded_key, algorithm)
            return JsonResponse({'access_token' : token.decode('UTF-8')}, status = 200)
