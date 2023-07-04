from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('search_results/', views.search_results, name='search_results'),
    path('udemy_view/', views.udemy_view, name='udemy'),
    path('youtube_view/', views.youtube_view, name='youtube'),
]
