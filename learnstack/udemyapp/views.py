import requests
from django.shortcuts import render
from learnstack.settings.base import UDEMY_ACCESS_TOKEN
from youtubeapp.models import SearchQuery
from .models import UdemyCourse
def search_form(request):
    return render(request, 'search_form.html')

def search_results(request):
    query = request.GET.get('query')
    access_token = UDEMY_ACCESS_TOKEN
    search_url = f'https://www.udemy.com/api-2.0/courses/?search={query}&page_size=15'
    # breakpoint()
    
    headers = {'Authorization': f'Bearer {access_token}'}
    search_response = requests.get(search_url, headers=headers)
    if search_response.status_code == 200:
        results = []
        api_results = search_response.json().get('results')
        
        for api_result in api_results:
            title = api_result.get('title')
            description = api_result.get('description')

            thumbnail = api_result.get('image_480x270')
            url = api_result.get('url') 
            
            course = UdemyCourse.objects.create(title=title, description=description,thumbnail=thumbnail).save()
            
            print(course)
            video_url = get_video_url(url)
              
            result = {
                'title': title,
                'description': description,
                'thumbnail': thumbnail,
                'url': url,
            }
            results.append(result)
        return render(request, 'search_results.html', {'results': results})
   

    return render(request, 'error.html', {'error_message': 'An error occurred.'})



def get_video_url(course_url):
    
    print(course_url,"================")