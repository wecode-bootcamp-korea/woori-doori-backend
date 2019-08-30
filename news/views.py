from django.http import JsonResponse
from django.views import View
from .models import News, Tag
import json

class TagView(View):
	
	def get(self,request):
		tag_data = list(Tag.objects.values())
		return JsonResponse(tag_data, safe=False, status=200)	

	def post(self,request):
		data = json.loads(request.body)
		
		try:
			new_tag = Tag.objects.create(tag = data['tag'])
		except:
			return JsonResponse({'message': 'the tag you tried already exists!'}, safe=False, status=405)
		
		return JsonResponse({'message':'new tag was created!'}, safe=False, status=200)	
		


class NewsView(View):
	
	def get(self,request):
		news_data = News.objects.values()
		result = []
		for delta in news_data:
			result.append({
							'id'        : delta['id'],
							'title'     : delta['title'],
							'tag_id'    : Tag.objects.get(pk = delta['tag_id']).id,
							'tag'       : Tag.objects.get(pk = delta['tag_id']).tag,
							'image_url' : delta['image_url'],
							'content'   : delta['content'],
						  })
			
		return JsonResponse(result, safe=False, status=200)

	def post(self,request):
		data = json.loads(request.body)
				
		try:
			new_tag = Tag.objects.get(pk = data['tag'])
		except:
			return JsonResponse({'message':'please check the tag field.'}, safe=False, status=405)
		
		news_data = News(
				title = data['title'],
				tag = new_tag,
				image_url = data['image_url'],
				content = data['content'],
				)
		news_data.save()

		return JsonResponse({'message':'posting success!'}, safe=False, status=200)
