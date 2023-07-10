from django.db import models

# Create your models here.
class SearchQuery(models.Model):
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class YouTubeVideo(models.Model):
    search_query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name='youtube_videos')
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_id = models.CharField(max_length=20)
    thumbnail_url = models.URLField()   

class UdemyCourse(models.Model):
    search_query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name='udemy_courses')
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    thumbnail = models.URLField()
    link = models.URLField()