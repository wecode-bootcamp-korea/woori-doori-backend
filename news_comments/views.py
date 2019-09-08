from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import NewsComments
from users.models import User
from news.models import News
from users.utils import validate_login
import json

class NewsCommentsView(View):

	def get(self, request, news_id):
		if NewsComments.objects.filter(news_id = news_id, is_deleted = False).exists() is False:
			return JsonResponse({'message':'COMMENT_NOT_EXIST'}, safe = False, status = 401)
		
		comment_data = NewsComments.objects.select_related('news').filter(news = news_id,is_deleted = False).values()
			
		data = [{
				'user_id'   : item['user_id'],
				'user_name' : User.objects.get(id = item['user_id']).user_id,
				'news_id'   : item['news_id'],
				'news_title': News.objects.get(id = item['news_id']).title,
				'comment_id': item['id'],
				'image_url' : item.get('image_url',''),
				'content'   : item['content'],
				'updated_at': item['updated_at'],	
				} for item in comment_data]
		
		return JsonResponse({'total':len(comment_data), 'data' : data }, safe = False, status = 200)
	
	@validate_login
	def post(self, request, news_id):
		data = json.loads(request.body)
		
		try:
			login_user = User.objects.get(pk = data['user_id'])
			news_page  = News.objects.get(pk = news_id)

		except User.DoesNotExist:
			return JsonResponse({'message':'INVALID_INPUT'}, status = 401)
		except News.DoesNotExist:
			return JsonResponse({'message':'NEWS_NOT_EXIST'}, status = 401)
		if data.get('content') is None or '':
			return JsonResponse({'message':'FILL_COMMENT'}, status = 401)

		NewsComments(
				user      = login_user,
				news      = news_page,
				image_url = data.get('image_url',''),
				content   = data['content'],
				).save()
	
		return HttpResponse(status = 200)

class UpdateCommentsView(View):
	
	def get(self, request, news_id):
		user_comments = NewsComments.objects.select_related('news').filter(news = news_id).values()
		return JsonResponse(list(user_comments), safe = False, status = 200)
	
	@validate_login
	def post(self, request, news_id):
		data = json.loads(request.body)
		user_comments = NewsComments.objects.select_related('news').filter(news = news_id).filter(user = data['user_id'])
		
		if data.get('content') is None or '':
			return JsonResponse({'message':'FILL_COMMENT'}, status = 401)

		try:
			if user_comments.exists():
				comment_to_update = user_comments.get(pk = data['id'])
				comment_to_update.content = data['content']
				comment_to_update.is_deleted = False
				comment_to_update.save()
				return HttpResponse(status = 200)
			else:
				return JsonResponse({'message':'METHOD_NOT_ALLOWED'}, status = 405)
		except NewsComments.DoesNotExist:
			return JsonResponse({'message':'COMMENT_NOT_EXIST'}, status = 401)
	
	@validate_login	
	def delete(self, request, news_id):
		data = json.loads(request.body)
		user_comments = NewsComments.objects.select_related('news').filter(news = news_id).filter(user = data['user_id'])

		try:
			if user_comments.exists():
				comment_to_delete = user_comments.get(pk = data['id'])
				comment_to_delete.is_deleted = True
				comment_to_delete.save()
				return HttpResponse(status = 200)
			else:
				return JsonResponse({'message':'METHOD_NOT_ALLOWED'}, status = 405)
		except NewsComments.DoesNotExist:
			return JsonResponse({'meesage':'COMMENT_NOT_EXIST'}, status = 401)
