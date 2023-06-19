from django.shortcuts import render
from googleapiclient.discovery import build
from .models import SearchQuery, YouTubeVideo
from learnstack.settings import YOUTUBE_API_KEY
from django.views.decorators.csrf import csrf_exempt,csrf_protect


def home(request):
    return render(request, 'front_page.html')


@csrf_exempt 
def search(request):
    if request.method == 'POST':
        
        query = request.POST.get('query', '')

        # Save the search query in the database
        SearchQuery.objects.create(query=query)

        # Call the YouTube API to fetch search results
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=15
        ).execute()

        # Clear existing video data from the database
        YouTubeVideo.objects.all().delete()

        # Store the search results in the database
        for search_result in search_response.get('items', []):
            video_id = search_result.get('id', {}).get('videoId', '')
            title = search_result.get('snippet', {}).get('title', '')
            description = search_result.get('snippet', {}).get('description', '')
            thumbnail_url = search_result.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', '')
            YouTubeVideo.objects.create(
                video_id=video_id,
                title=title,
                description=description,
                thumbnail_url=thumbnail_url
            )

    videos = YouTubeVideo.objects.all()
    return render(request, 'youtube_result.html', {'videos': videos})









