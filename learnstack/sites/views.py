from django.http import HttpResponse
import requests
from django.shortcuts import render
from learnstack.settings.base import UDEMY_ACCESS_TOKEN, YOUTUBE_API_KEY
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.discovery import build
from sites.models import SearchQuery, UdemyCourse, YouTubeVideo

YOUTUBE_MAX_RESULTS = 15
UDEMY_PAGE_SIZE = 15

def frontpage(request):
    return render(request, 'dashboard/index.html')


def search_youtube_videos(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=YOUTUBE_MAX_RESULTS
    ).execute()

    YouTubeVideo.objects.all().delete()

    for search_result in search_response.get('items', []):
        video_id = search_result.get('id', {}).get('videoId', '')
        title = search_result.get('snippet', {}).get('title', '')
        description = search_result.get('snippet', {}).get('description', '')
        thumbnails = search_result.get('snippet', {}).get('thumbnails', {})
        thumbnail_url = (
            thumbnails.get('maxres', {}).get('url', '') or
            thumbnails.get('high', {}).get('url', '') or
            thumbnails.get('default', {}).get('url', '')
        )
        YouTubeVideo.objects.create(
            video_id=video_id,
            title=title,
            description=description,
            thumbnail_url=thumbnail_url
        )

    videos = YouTubeVideo.objects.all()
    return videos


def search_udemy_courses(query):
    access_token = UDEMY_ACCESS_TOKEN
    search_url = f'https://www.udemy.com/api-2.0/courses/?search={query}&page_size={UDEMY_PAGE_SIZE}'
    headers = {'Authorization': f'Bearer {access_token}'}
    search_response = requests.get(search_url, headers=headers)

    if search_response.status_code == 200:
        results = []
        api_results = search_response.json().get('results')
        UdemyCourse.objects.all().delete()

        for api_result in api_results:
            title = api_result.get('title')
            price = api_result.get('price')
            thumbnail = api_result.get('image_480x270')
            url = api_result.get('url')
            UdemyCourse.objects.create(
                title=title,
                thumbnail=thumbnail,
                link=url,
                price=price
            )

            result = {
                'title': title,
                'price': price,
                'thumbnail': thumbnail,
                'url': url,
            }
            results.append(result)

        return results


@csrf_exempt
def search_results(request):
    if request.method == 'POST':
        
        selected_category = request.POST.get('select_category')
        query = request.POST.get('search_input')

        if selected_category == 'youtube':
            SearchQuery.objects.create(query=query)
            videos = search_youtube_videos(query)
            return render(request, 'dashboard/index.html', {'videos': videos})

        elif selected_category == 'udemy':
            SearchQuery.objects.create(query=query)
            results = search_udemy_courses(query)
            return render(request, 'dashboard/index.html', {'results': results})

        elif selected_category == 'categories':
            SearchQuery.objects.create(query=query)
            videos = search_youtube_videos(query)
            results = search_udemy_courses(query)
            return render(request, 'dashboard/index.html', {'results': results, 'videos': videos, 'query': query})

    return HttpResponse('Invalid request method')


def udemy_view(request):
    query = request.POST.get('search_input')
    results = UdemyCourse.objects.filter(title__icontains=query)
    return render(request, 'udemy.html', {'results': results})


def youtube_view(request):
    query = request.POST.get('search_input')
    videos = YouTubeVideo.objects.filter(title__icontains=query)
    return render(request, 'youtube.html', {'videos': videos})
