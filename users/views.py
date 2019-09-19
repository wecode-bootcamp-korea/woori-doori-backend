import bcrypt
import json
import jwt
import datetime
import requests
import settings

from django.views           import View
from django.http            import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, SocialPlatform

class SignUpView(View):
    FIELDS = {
        "user_id"  : "FILL_USERID",
        "name"     : "FILL_USERNAME",
        "password" : "FILL_USER_PASSWORD",
        "email"    : "FILL_USER_EMAIL"
    }

    def _validate_user_input(self, data):
        for field, message in self.FIELDS.items():
            if data.get(field) is None or len(data[field]) == 0:
                return {"message" : message}

    def post(self, request):
        user_data        = json.loads(request.body)
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

class SignInView(View):

    def post(self, request):
        user_data = json.loads(request.body)

        if user_data.get('user_id') is None or len(user_data['user_id']) == 0:
            return JsonResponse({'message' : 'ID_MISSING'}, status = 401)

        if user_data.get('password') is None or len(user_data['password']) == 0:
            return JsonResponse({'message' : 'PASSWORD_MISSING'}, status = 401)

        try:
            user = User.objects.get(user_id = user_data['user_id'])
        except User.NotExist:
            return JsonResponse({'message' : 'USER_NOT_EXIST'}, status = 401)

        if bcrypt.checkpw(user_data['password'].encode('utf-8'), user.password.encode('utf-8')):
            payload = {
                'id'  : user.id,
                'exp' : datetime.datetime.now() + datetime.timedelta(days = 1),
            }

            encoded_key = settings.SECRET_KEY
            algorithm   = 'HS256'
            token       = jwt.encode(payload, encoded_key, algorithm)

            return JsonResponse({'access_token' : token.decode('utf-8')}, safe = False, status = 200)
        else:
            return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 401)

class GoogleAuthView(View):
    def _get_google_user_id(self, access_token):
        google_api_url   = f"https://oauth2.googleapis.com/tokeninfo?id_token={access_token}"
        response         = requests.get(google_api_url, timeout=3)
        google_user_info = response.json()
        google_user_id   = google_user_info['sub']

        return google_user_id

    def post(self, request):
        google_auth_token = request.headers.get("Authorization", None)

        if google_auth_token:
            return JsonResponse({"ERROR": "GOOGLE_AUTH_TOKEN_REQUIRED"}, status=400)

        google_user_id = self._get_google_user_id(google_access_token)
        encoded_key    = settings.SECRET_KEY
        jwt_algorithm  = 'HS256'

        if User.objects.filter(social_user_id = google_user_id).exists():
            user    = User.objects.get(social_user_id = google_user_id)
            payload = {
                'id'        : user.id,
                'google_id' : google_user_id,
                'exp'       : datetime.datetime.now() + datetime.timedelta(days = 1)
            }
            token = jwt.encode(payload, encoded_key, jwt_algorithm)

            return JsonResponse({'access_token' : token.decode('UTF-8')}, status = 200)
        else:
            new_user_info = User(
                social_user_id = user['sub'],
                social         = SocialPlatform.objects.get(platform = 'google')
            )
            new_user_info.save()
            
            payload = {
                'id'        : new_user_info.id,
                'google_id' : google_user_id,
                'exp'       : datetime.datetime.now() + datetime.timedelta(days = 1),
            }
            token = jwt.encode(payload, encoded_key, algorithm)

            return JsonResponse({'access_token' : token.decode('UTF-8')}, status = 200)

class KakaoAuthView(View):
    def get(self, request):
        ## 위의 구글 엔드포인트랑 동일하게 refactoring 하면 됩니다.

        access_token = request.headers["Authorization"]
        headers = {'Authorization' : f'Bearer {access_token}'}
        url = "https://kapi.kakao.com/v1/user/me"
        response = requests.request("POST", url, headers = headers)
        user = response.json()
        encoded_key = settings.SECRET_KEY
        algorithm = 'HS256'
        ONE_DAY = 60 * 60 * 24

        if User.objects.filter(social_user_id = user['id']).exists():
            user_info = User.objects.get(social_user_id = user['id'])
            payload = {
                'id' : user_info.id,
                'kakao_id' : user['id'],
                'exp': datetime.datetime.now() + datetime.timedelta(seconds = ONE_DAY),
                }
            token = jwt.encode(payload, encoded_key, algorithm)
            return JsonResponse({'access_token' : token.decode('UTF-8')}, status = 200)

        else:
            new_user_info = User(
                    social_user_id = user['id'],
                    social = SocialPlatform.objects.get(platform = 'kakao')
                    )
            new_user_info.save()
            
            payload = {
                'id' : User.objects.get(social_user_id = user['id']).id,
                'kakao_id' : user['id'],
                'exp': datetime.datetime.now() + datetime.timedelta(seconds = ONE_DAY),
                }
            token = jwt.encode(payload, encoded_key, algorithm)
            return JsonResponse({'access_token' : token.decode('UTF-8')}, status = 200)
