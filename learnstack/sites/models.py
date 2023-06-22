from django.db import models

# Create your models here.
class SearchQuery(models.Model):
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_id = models.CharField(max_length=20)
    thumbnail_url = models.URLField()

class UdemyCourse(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    link = models.URLField()

    def __str__(self):
        return self.title