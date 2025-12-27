from django.urls import path

from . import views

urlpatterns = [

    path('youtube/search', views.search, name='search'),

    path('youtube/downl/', views.downloader, name='downloader'),

]
