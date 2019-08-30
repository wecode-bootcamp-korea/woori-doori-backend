from django.db import models

class Tag(models.Model):
	
	tag = models.CharField(max_length = 100, null = False, unique = True)
	created_at = models.DateField(auto_now_add = True)
	updated_at = models.DateField(auto_now = True)

	class Meta:
		db_table = 'tag'

class News(models.Model):

	title = models.CharField(max_length = 200, null = False)
	tag = models.ForeignKey(Tag, on_delete = models.CASCADE)
	image_url = models.URLField(max_length = 200, null = True)
	content = models.TextField(null = False)
	created_at = models.DateField(auto_now_add = True)
	updated_at = models.DateField(auto_now = True)
	
	class Meta:
		db_table = 'news'

