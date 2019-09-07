from django.db import models

class Users(models.Model):
	
	user_id = models.CharField(max_length = 15, unique = True, null = False)
	user_name = models.CharField(max_length = 15, null = True)
	user_password = models.CharField(max_length = 200, null = True)
	user_email = models.EmailField(max_length = 50, unique = True,  null = True)
	user_photo = models.URLField(max_length = 2500, null = True)
	user_profile = models.CharField(max_length = 300, null = True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	
	class Meta:
		db_table = 'users'
