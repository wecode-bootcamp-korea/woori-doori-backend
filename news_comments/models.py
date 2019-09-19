from django.db import models
from users.models import User
from news.models import News

class NewsComments(models.Model):
	user       = models.ForeignKey(User, on_delete = models.CASCADE)
	news       = models.ForeignKey(News, on_delete = models.CASCADE)
	image_url  = models.URLField(max_length        = 2500, null      = True)
	is_deleted = models.BooleanField(default       = False, null     = True)
	content    = models.TextField(null             = False)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now     = True)

	class Meta:
		db_table = 'news_comments'
