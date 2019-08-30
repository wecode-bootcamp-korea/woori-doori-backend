from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import *
from WooriDooriBackEnd import settings
import json
import bcrypt
import pdb
import datetime
import jwt


class SignUp(View):
    def post(self,request):
        data = json.loads(request.body)
        user_id = data["user_id"]
        password = data["password"]
        ch_password = data["ch_password"]
        
        if User.objects.filter(user_id = user_id).exists():
            return JsonResponse({"message":"EXISTED_ID"}, status = 401)
        elif password != ch_password:
            return JsonResponse({"message":"MISMATCHED_PASSWORD"}, status = 401)
        else:
            bytes_password = bytes(password, "UTF-8")
            hashed_password = bcrypt.hashpw(bytes_password, bcrypt.gensalt())   

            new_user = User(
                    user_id = data["user_id"],         
                    password =hashed_password.decode("UTF-8"),
                    email = data["email"]
                    )   
            new_user.save()
            return JsonResponse({"message":"SUCCESS"}, status = 200)

class LogIn(View):
    def post(self,request):
        data = json.loads(request.body)
        user_id = data["user_id"]
        password = data["password"]

        
        if User.objects.filter(user_id = user_id).exists():
            got_user_info = User.objects.filter(user_id = user_id).get()
        else:
            return JsonResponse({"message":"WRONG_ID"}, status = 401)
        
        if bcrypt.checkpw(password.encode("utf-8"), got_user_info.password.encode('utf-8')):
            user_id = got_user_info.id
            payload = {
                'user_pk' : got_user_info.id,
                'exp' : datetime.datetime.now() + datetime.timedelta(seconds = 60 * 60 * 24)
            }
            encryption_secret = settings.SECRET_KEY 
            algorithm = 'HS256'
            encoded_token = jwt.encode(payload, encryption_secret, algorithm)

            return JsonResponse({"access_token":encoded_token.decode('utf-8')}, status = 200)
        else:
            return JsonResponse({"message":"WRONG_PASSWORD"}, status = 401)
