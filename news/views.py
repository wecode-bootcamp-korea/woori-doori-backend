from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import News, Tags
import json
import random
import math

class TagView(View):
	def get(self, request):
		tag_data = [{
			'id'  : tag['id'],
			'tag' : tag['tag'],
		} for tag in Tags.objects.values()]

		return JsonResponse(tag_data, safe = False, status = 200)
	
	def post(self,request):
		data = json.loads(request.body)
		tags = Tags.objects

		if tags.filter(tag = data['tag']).exists():
			return JsonResponse({'message':'INPUT_EXISTS'}, status = 409)

		tags.objects.create(tag = data['tag'])

		return HttpResponse(status = 200)

class NewsListView(View):
	def get(self, request):
		offset = int(request.GET.get('offset',0))
		limit  = int(request.GET.get('limit', 10))
		tag_id = int(request.GET.get('tag_id', None))
				
		news = News.objects.select_related('tag')
		
		if tag_id is None: 
			total_count = news.all().count()
			news        = news.values()
		else:
			total_count = news.filter(tag_id = tag_id).count()
			news        = news.filter(tag_id = tag_id).values()
			
		news = [{
			'id'        : data['id'],
			'title'     : data['title'],
			'tag_id'    : data['tag_id'],
			'tag'       : Tags.objects.get(pk = data['tag_id']).tag,
			'image_url' : data['image_url'],
			'content'   : data['content']
		} for data in news[offset:limit]]

		response = [{'total_count' : total_count, 'news_data': news_data }]

		return JsonResponse(response, safe = False, status = 200)
		
	def post(self, request):
	    data = json.loads(request.body)
				
	    try:
	    	tag = Tags.objects.get(pk = data['tag_id'])
	    except Tags.DoesNotExist:
	        return JsonResponse({'message':'TAG_NOT_EXIST'}, status = 405)
	
		News(
			title     = data['title'],
			tag       = new_tag,
			image_url = data.get('image_url',''),
			content   = data['content'],
		).save()

	    return HttpResponse(status = 200)

class NewsView(View):
	def get(self, request, news_id):
		try:
			target         = News.objects.get(pk = news_id)
			target_content = {
				'id'        : target.id,
				'title'     : target.title,
				'tag_id'    : target.tag_id,
				'tag'       : Tags.objects.get(pk = target.tag_id).tag,
				'image_url' : target.image_url,
				'content'   : target.content,
			}

			return JsonResponse(target_content, safe = False, status = 200)
		except News.DoesNotExist:
			return JsonResponse({'message': 'NEWS_NOT_EXIST'}, status = 401)
