from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sites.models import SearchQuery, UdemyCourse, YouTubeVideo
from sites.utils import search_youtube_videos, search_udemy_courses
from datetime import timedelta
from django.utils import timezone
import threading
import time


def frontpage(request):
    return render(request, 'dashboard/index.html')


@csrf_exempt
def search_results(request):
    if request.method == 'POST':
        selected_category = request.POST.get('select_category')
        query = request.POST.get('search_input')
        if selected_category == 'youtube':
            youtube_videos_exist = YouTubeVideo.objects.filter(search_query__query=query).exists()
            if youtube_videos_exist:
                videos = YouTubeVideo.objects.filter(search_query__query=query)          
            else:
                new_search_query = SearchQuery.objects.create(query=query)
                youtube_thread = threading.Thread(target=search_youtube_videos, args=(query, new_search_query,))
                youtube_thread.start()
                youtube_thread.join()
                videos = YouTubeVideo.objects.filter(search_query=new_search_query)
            return render(request, 'dashboard/index.html', {'videos': videos,'query': query})

        elif selected_category == 'udemy':
            udemy_courses_exist = UdemyCourse.objects.filter(search_query__query=query).exists()
            if udemy_courses_exist:
                results = UdemyCourse.objects.filter(search_query__query=query)

            else:
                new_search_query_udemy = SearchQuery.objects.create(query=query)
                udemy_thread = threading.Thread(target=search_udemy_courses, args=(query, new_search_query_udemy,))
                udemy_thread.start()
                udemy_thread.join()

                results = UdemyCourse.objects.filter(search_query=new_search_query_udemy)
            return render(request, 'dashboard/index.html', {'results': results, 'query': query})

        elif selected_category == 'categories':
            youtube_videos_exist = YouTubeVideo.objects.filter(search_query__query=query).exists()
            udemy_courses_exist = UdemyCourse.objects.filter(search_query__query=query).exists()

            if youtube_videos_exist and udemy_courses_exist:
                videos = YouTubeVideo.objects.filter(search_query__query=query)
                results = UdemyCourse.objects.filter(search_query__query=query)
            else:
                new_search_query_youtube = SearchQuery.objects.create(query=query)
                new_search_query_udemy = SearchQuery.objects.create(query=query)
                youtube_thread = threading.Thread(target=search_youtube_videos, args=(query, new_search_query_youtube,))
                udemy_thread = threading.Thread(target=search_udemy_courses, args=(query, new_search_query_udemy,))
                youtube_thread.start()
                udemy_thread.start()
                youtube_thread.join()
                udemy_thread.join()

                videos = YouTubeVideo.objects.filter(search_query=new_search_query_youtube)
                results = UdemyCourse.objects.filter(search_query=new_search_query_udemy)
        return render(request, 'dashboard/index.html', {'videos': videos, 'results': results, 'query': query})

    return HttpResponse('Invalid request method')


def udemy_view(request):
    query = request.POST.get('search_input')
    results = UdemyCourse.objects.filter(search_query__query=query)
    return render(request, 'udemy.html', {'results': results})


def youtube_view(request):
    query = request.POST.get('search_input')
    videos = YouTubeVideo.objects.filter(search_query__query=query)
    return render(request, 'youtube.html', {'videos': videos})