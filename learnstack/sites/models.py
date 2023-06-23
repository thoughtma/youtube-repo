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
    price = models.CharField(max_length=10)
    thumbnail = models.URLField()
    link = models.URLField()

    def __str__(self):
        return self.title