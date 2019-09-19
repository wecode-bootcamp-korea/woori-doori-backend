import json

from django.shortcuts import render
from django.http      import JsonResponse, HttpResponse
from django.views     import View

from .models import (
    Category, 
    CategoryItem, 
    RecipeItem
)

RETURN_MESSAGE = {
    "DOES_NOT_EXIST": "데이터가 존재하지 않습니다." 
}

class CategoryView(View):
    def get(self, request):
        category_list = (
            CategoryItem.objects.order_by('id')
            .select_related('category')
            .values(
                'id',
                'name',
                'category__name'
            )
        )

        return JsonResponse({"result" : category_list}, safe=False, status=200)

class RecipeView(view):
    def get(self, request, recipe_id):
        try:
            fields = [
				'recipe_number', 'title', 'name', 'method', 
				'image', 'category_item__item_number','category_item__name'
			]
            result = RecipeItem.objects.values(*fields).get(id=recipe_id) # where id = 1

            return JsonResponse({ "recipe" : result}, safe = False, status=200) 
        except RecipeItem.DoesNotExist:
            return JsonResponse({"message": RETURN_MESSAGE["DOES_NOT_EXIST"]}, status=404)

class RecipeListView(View):
	KOREAN = 1

    def get(self, request):
        category_id = int(request.GET.get("category_id", self.KOREAN))
        recipe_id   = int(request.GET.get("recipe_id", None))
        offset      = int(request.GET.get("offset", 0))
        limit       = int(request.GET.get("limit", 1))

        try:
            total_count = RecipeItem.objects.filter(category_item__item_number = category_item_number).count()
            fields      = [
				'recipe_number', 'title', 'name', 'method', 
				'image', 'category_item__item_number','category_item__name'
			]
            result = RecipeItem.objects.filter(category_item__item_number=category_item_number).values(*fields)[offset:limit]
            return JsonResponse({ "total_count" : total_count, "result": result}, safe = False, status=200) 
        except CategoryItem.DoesNotExist:
            return JsonResponse({"message": RETURN_MESSAGE["DOES_NOT_EXIST"]}, status=404)
