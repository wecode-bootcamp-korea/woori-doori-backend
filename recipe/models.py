from django.db import models
import datetime
from django.utils import timezone


class Category(models.Model):
    category_no = models.IntegerField()
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category_no


class CategoryItem(models.Model):
    item_no = models.IntegerField()
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_no


class RecipeItem(models.Model):
    recipe_no = models.IntegerField()
    title = models.CharField(max_length=500)
    method = models.CharField(max_length=2000)
    image = models.URLField(max_length=300, null=True)
    categoryItem = models.ForeignKey(CategoryItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


