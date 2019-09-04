from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Category, CategoryItem, RecipeItem
import json
import ipdb as pdb
import logging


class CategoryView(View):
    RETURN_MESSAGE = {
        "DOES_NOT_EXIST": "데이터가 존재하지 않습니다." 
    }
   
    def get(self, request):
        # pdb.set_trace()
        try:
            categoryList = list(CategoryItem.objects.order_by('item_no').select_related('category').values(
                                'item_no',
                                'name',
                                'category__name'
                            ))
            return JsonResponse(categoryList, safe=False, status=200)
        except CategoryItem.DoesNotExist:
            return JsonResponse(RETURN_MESSAGE["DOES_NOT_EXIST"], safe=False, status=204)
    
    # 추후 삭제할 코드
    def initDBForTest():
        category_default = [
            '나라별', '식자재별'
        ]
        categoryItem_default = [
            ['한식', '중식', '양식', '일식'],
            ['야채', '닭고기', '소고기', '돼지고기']
        ]
        categoryItemIndex = 0

        for index in range(len(category_default)):
            category_table = Category(category_no=index+1,
                                    name = category_default[index])
            category_table.save()

        for indexA in range(len(categoryItem_default)):
            for indexB in range(len(categoryItem_default[indexA])):
                category = Category.objects.get(name=category_default[indexA])
                categoryItem_table = CategoryItem(item_no=categoryItemIndex,
                                        name=categoryItem_default[indexA][indexB], 
                                        category=category)
                categoryItem_table.save()
                categoryItemIndex = categoryItemIndex + 1


class RecipeView(View):
    RETURN_MESSAGE = {
        "DOES_NOT_EXIST": "데이터가 존재하지 않습니다." 
    }

    def get(self, request):
        COMMAND_TYPE = {
           "RECIPE_DETAIL": 1,
           "CATEGORY_RECIPES": 2,
           "RECENT_RECIPES": 3,
        }
        
        # pdb.set_trace()
        data = json.loads(request.body)
        command = data["command"]
        recipe_no = data["recipe_no"]
        categoryItem_no = data["categoryItem_no"]
        start_no = data["start_no"]
        recipe_cnt = data["recipe_cnt"]

        try:
            if(command == COMMAND_TYPE["RECIPE_DETAIL"]):
                result = list(RecipeItem.objects.filter(recipe_no=recipe_no).values(
                                'recipe_no',
                                'title',
                                'method',
                                'image',
                                'categoryItem__item_no',
                                'categoryItem__name'))[0]
            elif(command == COMMAND_TYPE["CATEGORY_RECIPES"]):
                recipe_count = RecipeItem.objects.filter(categoryItem__item_no=categoryItem_no).count()
                last_no =  recipe_count if (start_no+recipe_cnt) > recipe_count  else (start_no+recipe_cnt) 
                result = list(RecipeItem.objects.filter(categoryItem__item_no=categoryItem_no).values(
                                'recipe_no',
                                'title',
                                'image',
                                'categoryItem__item_no',
                                'categoryItem__name'))[start_no:last_no]
            elif(command == COMMAND_TYPE["RECENT_RECIPES"]):
                recipe_count = RecipeItem.objects.order_by('-created_at').count()
                last_no =  recipe_count if (start_no+recipe_cnt) > recipe_count  else (start_no+recipe_cnt) 
                result = list(RecipeItem.objects.order_by('-created_at').values(
                                'recipe_no',
                                'title',
                                'image',
                                'categoryItem__item_no',
                                'categoryItem__name'))[start_no:last_no]
            else:
                return HttpResponse(status=400)

            return JsonResponse(result, safe=False, status=200)
            
        except CategoryItem.DoesNotExist:
            return JsonResponse(RETURN_MESSAGE["DOES_NOT_EXIST"], safe=False, status=204)

    
    # 추후 삭제할 코드
    def initDBForTest():
        recipe_category = ["한식", "한식", "중식", "양식", "양식", "일식", "야채", "소고기", "닭고기", "소고기", "돼지고기"]
        recipe_title = "생활습관병을 예방하는 '건강식' 시리즈 첫 회 테마는 고혈압을 예방하는 저염요리."
        recipe_method = "닭다리살을 도마 위에 펼쳐 놓고 한가운데 오목한 부분에서 반으로 잘라 4토막으로 만듭니다.\n고기 두께를 균등하게 하기 위해 얇은 부분에 맞추어 두꺼운 부분을 안에서 바깥쪽으로 깔집을 넣어 원래 고기의 2배 정도 크기로 폅니다.\n4토막을 모두 얇게 펴고 녹말가루를 듬뿍 뿌린 뒤 덧가루는 털어냅니다.\n작은 그릇에 사과주스, 간장, 설탕, 식초, 간 생강을 넣고 섞어 데리야키 소스를 만들어 놓습니다.\n큰 프라이팬에 기름을 두르고 껍질을 밑으로 해서 닭고기를 나란히 놓고 가끔 움직이면서 중불에서 노릇하게 굽습니다.\n뒤집어서 뚜껑을 덮고 약한 불로 4 분 정도 굽습니다. 대나무 꼬치나 포크로 찔러보아 맑은 국물이 나오면 일단 프라이팬에서 닭고기를 꺼냅니다.\n프라이팬의 기름을 닦아내고 만들어 놓은 소스를 넣어 데워지면 구운 닭고기를 넣어 버무립니다."
        recipe_image = ["https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_170428_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_190627_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_190222_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_171222_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_180126_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_140725_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_170623_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_180727_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_180629_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_180427_l.jpg",
                        "https://www3.nhk.or.jp/nhkworld/en/radio/cooking/update/meal_170728_l.jpg"]
 
        for index in range(len(recipe_category)):
            categoryItem = CategoryItem.objects.get(name=recipe_category[index])
            recipe_item = RecipeItem(
                            recipe_no = index+1,
                            title = recipe_title,
                            method = recipe_method,
                            image = recipe_image[index],
                            categoryItem = categoryItem)
            recipe_item.save()

# 추후진행예정
class Comments(View):

    def post(self, request):
        data = json.loads(request.body)
        return JsonResponse({"message":"OK"}, status = 200)

    def get(self, request):
        return JsonResponse({"message":"OK"}, status = 200)

    def options(self, request):
        return JsonResponse({"message":"OK"}, status = 200)


