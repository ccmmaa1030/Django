from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=20)
    summary = models.TextField()
    running_time = models.IntegerField()
    director = models.CharField(max_length=20)
    genre = models.CharField(max_length=20)
    opening_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
