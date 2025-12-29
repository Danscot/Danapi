from django.urls import path

from . import views

urlpatterns = [

    path('wallpaper/downl', views.download, name='download'),


]
