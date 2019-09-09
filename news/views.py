from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import News, Tags
import json
import random
import math

class TagView(View):
	
	def get(self, request):
		tag_data = [{
	                 'id': tag['id'],
	                 'tag': tag['tag'],
					} for tag in Tags.objects.values()]
		return JsonResponse(tag_data, safe = False, status = 200)
	
	def post(self,request):
		data = json.loads(request.body)
		tags = Tags.objects
		if tags.filter(tag = data['tag']).exists():
			return JsonResponse({'message':'INPUT_EXISTS'}, status = 409)

		tags.objects.create(tag = data['tag'])
		return HttpResponse(status = 200)

class NewsView(View):

	def get(self, request):
		offset = int(request.GET.get('offset','0'))
		tag_num = int(request.GET.get('tag_num','0'))
				
		if offset >= len(News.objects.values()) or tag_num >= len(Tags.objects.values()):
			return JsonResponse({'message':'PAGE_NOT_FOUND'}, status = 404)
		
		raw_data = News.objects.select_related('tag')
		
		if tag_num is 0: 
			raw_data = raw_data.values()
		else:
			raw_data = raw_data.filter(tag_id = tag_num).values()
			
		news_data = [{
					  'id'        : data['id'],
					  'title'     : data['title'],
					  'tag_id'    : data['tag_id'],
					  'tag'       : Tags.objects.get(pk = data['tag_id']).tag,
					  'image_url' : data['image_url'],
					  'content'   : data['content'], }
					  for data in raw_data][offset:offset+10]
		response = [{'total' : len(raw_data), 'news_data': news_data }]
		return JsonResponse(response, safe = False, status = 200)
		
	def post(self, request):
	    data = json.loads(request.body)
				
	    try:
	        new_tag = Tags.objects.get(pk = data['tag_id'])
	    except Tags.DoesNotExist:
	        return JsonResponse({'message':'TAG_NOT_EXIST'}, status = 405)
	
	    news_data = News(
	                     title = data['title'],
			             tag = new_tag,
			             image_url = data.get('image_url',''),
			             content = data['content'],
			             ).save()
	    return HttpResponse(status = 200)

class DetailNewsView(View):
	
	def get(self, request, news_id):	
		if news_id is 0 or news_id > len(News.objects.values()):
			return JsonResponse({'message':'NEWS_NOT_EXIST'}, status = 401)
		try:
			target = News.objects.get(pk = news_id)
			target_content = {
							  'id'        : target.id,
							  'title'     : target.title,
							  'tag_id'    : target.tag_id,
							  'tag'       : Tags.objects.get(pk = target.tag_id).tag,
							  'image_url' : target.image_url,
							  'content'   : target.content,
							 }
	
		except News.DoesNotExist:
			return JsonResponse({'message': 'NEWS_NOT_EXIST'}, status = 401)
		
		return JsonResponse(target_content, safe = False, status = 200)

