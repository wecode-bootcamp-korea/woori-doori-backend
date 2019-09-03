from django.db import models
from users.models import Users

class Comments(models.Model):

	user_id = models.ForeignKey(Users, on_delete = models.CASCADE, null = True)
	image_url = models.URLField(max_length = 2500, null = True)
	is_deleted = models.BooleanField(default = False, null = True)
	content = models.TextField(null = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	class Meta:
		db_table = 'comments'
