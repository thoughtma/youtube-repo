from django.urls import path
from . import views

urlpatterns = [
    path('',views.frontpage, name='home'),
    path('search/', views.search_results, name='search_results'),
]