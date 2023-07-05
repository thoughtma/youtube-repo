from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sites.models import SearchQuery, UdemyCourse, YouTubeVideo
from sites.utils import search_youtube_videos, search_udemy_courses
import threading


def frontpage(request):
    return render(request, 'dashboard/index.html')


@csrf_exempt
def search_results(request):
    if request.method == 'POST':
        selected_category = request.POST.get('select_category')
        query = request.POST.get('search_input')

        if selected_category == 'youtube':
            SearchQuery.objects.create(query=query)

            youtube_thread = threading.Thread(target=search_youtube_videos, args=(query,))
            youtube_thread.start()

            videos = YouTubeVideo.objects.all()
            return render(request, 'dashboard/index.html', {'videos': videos})

        elif selected_category == 'udemy':
            SearchQuery.objects.create(query=query)

            udemy_thread = threading.Thread(target=search_udemy_courses, args=(query,))
            udemy_thread.start()

            results = UdemyCourse.objects.all()
            return render(request, 'dashboard/index.html', {'results': results})

        elif selected_category == 'categories':
            SearchQuery.objects.create(query=query)

            youtube_thread = threading.Thread(target=search_youtube_videos, args=(query,))
            udemy_thread = threading.Thread(target=search_udemy_courses, args=(query,))

            youtube_thread.start()
            udemy_thread.start()

            videos = YouTubeVideo.objects.all()
            results = UdemyCourse.objects.all()
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