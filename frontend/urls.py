from django.urls import path

from . import views

urlpatterns = [

    path('', views.home_page, name='home_page'),

    path('doc', views.doc_page, name="doc_page"),

    path("api", views.api_page, name="api_page")

]
