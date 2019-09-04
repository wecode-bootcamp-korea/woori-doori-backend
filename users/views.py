from django.views import View
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Users
from WooriDooriBackEnd import settings
import bcrypt
import json
import jwt
import datetime
import pdb


class SignupView(View):

    FIELDS = {
        "user_id" : "FILL_USERID",
		"user_name" : "FILL_USERNAME",
		"user_password" : "FILL_USER_PASSWORD",
		"user_email" : "FILL_USER_EMAIL"
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

        if Users.objects.filter(user_id = user_data['user_id']).exists():
            return JsonResponse({'message' : 'USER_EXISTS'}, status = 409)
            
        encrypted_pw = bcrypt.hashpw(bytes(user_data['user_password'], 'utf-8'), bcrypt.gensalt())
        
        Users(
                user_id       = user_data['user_id'],
                user_name     = user_data['user_name'],
                user_password = encrypted_pw.decode('utf-8'),
                user_email    = user_data['user_email'],
                user_photo    = user_data.get('user_photo', ""),
                user_profile  = user_data.get('user_profile', ""),
                ).save()

        return HttpResponse(status = 200)

class SigninView(View):
    def post(self, request):
#        pdb.set_trace()
        user_data = json.loads(request.body)

        if user_data.get('user_id') is None or len(user_data['user_id']) == 0:
            return JsonResponse({'message' : 'FILL_ID'}, status = 401)
	
        if user_data.get('user_password') is None or len(user_data['user_password']) == 0:
            return JsonResponse({'message' : 'FILL_PASSWORD'}, status = 401)

        try:
            user_info = Users.objects.get(user_id = user_data['user_id'])
		
        except ObjectDoesNotExist:
            return JsonResponse({'message' : 'USER_NOT_EXIST'}, status = 401)

        if bcrypt.checkpw(user_data['user_password'].encode('utf-8'), user_info.user_password.encode('utf-8')):
            payload = {
                'id': user_info.id,
                'exp': datetime.datetime.now() + datetime.timedelta(seconds = 60 * 60 * 24),
				}
            encoded_key = settings.SECRET_KEY
            token = jwt.encode(payload, f'{encoded_key}', algorithm='HS256')
            return JsonResponse({'access_token' : token.decode('utf-8')}, safe = False, status = 200)
        else:
            return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 401)
