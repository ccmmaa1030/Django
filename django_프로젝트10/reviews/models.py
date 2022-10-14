from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    movie_name = models.CharField(max_length=20)
    grade_choices = (
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    )
    grade = models.IntegerField(choices=grade_choices)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)