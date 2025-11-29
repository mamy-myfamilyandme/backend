from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 원하는 필드를 여기에 추가하세요
    nickname = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.email