import requests
from django.shortcuts import render

def search_form(request):
    return render(request, 'search_form.html')

def search_results(request):
    # breakpoint()
    query = request.GET.get('query')  # Retrieve user's search query
    access_token = 'UDEMY_ACCESS_TOKEN'
    search_url = f'https://www.udemy.com/api-2.0/courses/?search={query}&page_size=15'

    # Use the access token to make the search request
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

            # Get the video URL using the course URL or any other available method
            video_url = get_video_url(url)  # Implement this function to retrieve the video URL

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
    # Implement the logic to retrieve the video URL for the given course URL
    # You may need to parse the course URL or make additional API requests to get the video URL
    # Return the video URL

    return ''
