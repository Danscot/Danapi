from django.urls import path

from . import views

urlpatterns = [

    path('hanime/search', views.search, name='search'),


]
