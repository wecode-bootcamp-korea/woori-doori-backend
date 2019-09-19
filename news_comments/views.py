import json

from django.http  import JsonResponse, HttpResponse
from django.views import View

from .models      import NewsComments
from users.models import User
from news.models  import News
from users.utils  import validate_login

class NewsCommentsView(View):
	def get(self, request, news_id):
		offset = int(request.GET.get('offset', 0))
		limit  = int(request.GET.get('limit', 10))

		comment_data = NewsComments.objects.select_related('news').filter(news = news_id, is_deleted = False).values()
		total_count  = comment_data.count()
		data         = [{
			'user_id'   : item['user_id'],
			'user_name' : User.objects.get(id = item['user_id']).user_id,
			'news_id'   : item['news_id'],
			'news_title': News.objects.get(id = item['news_id']).title,
			'comment_id': item['id'],
			'image_url' : item.get('image_url',''),
			'content'   : item['content'],
			'updated_at': item['updated_at']
		} for item in comment_data.order_by('created_at').reverse()][offset:limit]
		
		return JsonResponse({'total': total_count, 'data' : data }, safe = False, status = 200)
	
	@validate_login
	def post(self, request, news_id):
		data = json.loads(request.body)

		try:
			login_user = request.user
			news_page  = News.objects.get(pk = news_id)
		except News.DoesNotExist:
			return JsonResponse({'message':'NEWS_NOT_EXIST'}, status = 404)

		if "content" not in data or len(data['content']) == 0:
			return JsonResponse({'message':'COMMENT_MISSING'}, status = 400)

		NewsComments(
			user      = login_user,
			news      = news_page,
			image_url = data.get('image_url',''),
			content   = data['content']
		).save()
	
		return HttpResponse(status = 200)

class UpdateCommentsView(View):
	@validate_login
	def post(self, request, comment_id):
		data = json.loads(request.body)
		
		try:
			user_comment = NewsComments.objects.get(id = comment_id, user = request.user)

			if "content" not in data or len(data['content']) == 0:
				return JsonResponse({'message':'COMMENT_MISSING'}, status = 400)

			user_comment.content = data['content']
			user_comment.save()

			return HttpResponse(status = 200)
		except NewsComments.DoesNotExist:
			return JsonResponse({'message':'COMMENT_NOT_EXIST'}, status = 401)
	
	@validate_login	
	def delete(self, request, comment_id):
		try:
			user_comment = NewsComments.objects.get(id = comment_id, user = request.user)
			user_comment.is_deleted = True
			user_comment.save()

			return HttpResponse(status = 200)
		except NewsComments.DoesNotExist:
			return JsonResponse({'meesage':'COMMENT_NOT_EXIST'}, status = 401)
