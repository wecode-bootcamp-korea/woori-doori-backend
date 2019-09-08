from django.db import models


class SocialPlatform(models.Model):
    platform = models.CharField(max_length = 20, default = 0)

    class Meta:
        db_table = "social_platform"

class User(models.Model):
    user_id        = models.CharField(max_length = 15, unique = True, null = False)
    name           = models.CharField(max_length = 15, null = True)
    password       = models.CharField(max_length = 200, null = True)
    email          = models.EmailField(max_length = 50, unique = True,  null = True)
    photo          = models.URLField(max_length = 200, null = True)
    profile        = models.CharField(max_length = 300, null = True)
    created_at     = models.DateTimeField(auto_now_add = True)
    updated_at     = models.DateTimeField(auto_now = True)
    social         = models.ForeignKey(SocialPlatform, on_delete = models.CASCADE, max_length = 20, blank = True, default = 1)
    social_user_id = models.CharField(max_length = 50, blank = True)

    class Meta:
        db_table = 'user'
