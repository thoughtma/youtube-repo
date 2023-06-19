from django.contrib import admin
from youtubeapp.models import SearchQuery, YouTubeVideo

# Register your models here.
admin.site.register(SearchQuery)
admin.site.register(YouTubeVideo)