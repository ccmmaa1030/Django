from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)