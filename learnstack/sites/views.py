import requests
from django.shortcuts import render
from learnstack.settings.base import UDEMY_ACCESS_TOKEN, YOUTUBE_API_KEY
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.discovery import build
from sites.models import SearchQuery, UdemyCourse, YouTubeVideo


def frontpage(request):
    return render(request, 'dashboard/index.html')


@csrf_exempt

def search_results(request):
    if request.method == 'POST':
        selected_category = request.POST.get('category')
        query = request.POST.get('search_input')
        results = []
        
        if selected_category in ['youtube', 'categories']:
           
            SearchQuery.objects.create(query=query)

            
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
            search_response = youtube.search().list(
                q=query,
                part='snippet',
                maxResults=15
            ).execute()

            
            for search_result in search_response.get('items', []):
                video_id = search_result.get('id', {}).get('videoId', '')
                title = search_result.get('snippet', {}).get('title', '')
                description = search_result.get('snippet', {}).get('description', '')
                thumbnail_url = search_result.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', '')
                result = {
                    'platform': 'YouTube',
                    'video_id': video_id,
                    'title': title,
                    'description': description,
                    'thumbnail_url': thumbnail_url
                }
                results.append(result)

        if selected_category in ['udemy', 'categories']:
            
            access_token = UDEMY_ACCESS_TOKEN
            search_url = f'https://www.udemy.com/api-2.0/courses/?search={query}&page_size=15'
            headers = {'Authorization': f'Bearer {access_token}'}
            search_response = requests.get(search_url, headers=headers)
            if search_response.status_code == 200:
                api_results = search_response.json().get('results')
                for api_result in api_results:
                    title = api_result.get('title')
                    price = api_result.get('price')
                    thumbnail = api_result.get('image_480x270')
                    url = api_result.get('url')
                    result = {
                        'platform': 'Udemy',
                        'title': title,
                        'price': price,
                        'thumbnail': thumbnail,
                        'url': url
                    }
                    results.append(result)

     

       

        return render(request, 'search_results.html', {'results': results})

    return render(request, 'error.html', {'error_message': 'Invalid request method.'})

            
        
        



    





