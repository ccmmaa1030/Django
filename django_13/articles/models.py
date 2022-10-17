from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    thumbnail = ProcessedImageField(upload_to='images/', blank=True,
                                    processors=[ResizeToFill(400, 300)],
                                    format='JPEDG',
                                    options={'quality': 80}
                                    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)