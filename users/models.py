from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length = 30, unique = True)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 50, unique = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'user'
