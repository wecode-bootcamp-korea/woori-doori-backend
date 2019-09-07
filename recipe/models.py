from django.db import models
import datetime
from django.utils import timezone

class Category(models.Model):
    category_number = models.IntegerField()
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CategoryItem(models.Model):
    item_number = models.IntegerField()
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RecipeItem(models.Model):
    recipe_number = models.IntegerField()
    title = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    method = models.CharField(max_length=2000)
    image = models.URLField(max_length=300, null=True)
    category_item = models.ForeignKey(CategoryItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


