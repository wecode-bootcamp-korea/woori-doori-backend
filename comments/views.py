from django.http import JsonResponse
from django.views import View
from .models import Comments
import json

class CommentsView(View):
	
	def get(self, request):
		
		return JsonResponse('hello!!!', safe=False, status=200)

