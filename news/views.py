from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import News, Tags
import json

class TagView(View):
	
	def get(self,request):
            tag_data = [{
	                 'id': tag['id'],
	                 'tag': tag['tag'],
		         } for tag in Tags.objects.values()]	
	    return JsonResponse(tag_data, safe = False, status = 200)	

	def post(self,request):
	    data = json.loads(request.body)
	    
	    if Tags.objects.filter(tag = data['tag']).exists():
	        return JsonResponse({'message': 'INPUT_EXISTS'}, status=409)
            
	    Tags.objects.create(tag = data['tag'])		
	    return HttpResponse(status=200)	

class NewsView(View):

	def get(self,request,tag_nums,nums):
	    raw_data = News.objects
		
	    if tag_nums > 4:
		return JsonResponse({'message': 'TAG_NOT_EXISTS'}, status = 400)
	    elif tag_nums == 0:
	        raw_data = raw_data.values()
	    else:
	        raw_data = raw_data.filter(tag_id=tag_nums).values()

	    news_data = [{
	                  'id'        : data['id'],
		          'title'     : data['title'],
		          'tag_id'    : data['tag_id'],
		          'tag'       : Tags.objects.get(pk = data['tag_id']).tag,
		          'image_url' : data['image_url'],
		          'content'   : data['content'],
		          } for data in raw_data][nums*10:nums*10+10]
	    return JsonResponse(news_data, safe = False, status = 200)

	def post(self,request):
	    data = json.loads(request.body)
				
	    try:
	        new_tag = Tags.objects.get(pk = data['tag_id'])
	    except:
	        return JsonResponse({'message':'INVALID_INPUT'}, status = 405)
	
	    news_data = News(
	                     title = data['title'],
			     tag = new_tag,
			     image_url = data['image_url'],
			     content = data['content'],
			     )
	    news_data.save()
	    return HttpResponse(status = 200)
