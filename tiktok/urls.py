from django.urls import path

from . import views

urlpatterns = [

    path('tiktok/download', views.downloader, name='tiktok_downl'),


]
