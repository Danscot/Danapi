from django.urls import path

from . import views

urlpatterns = [

    path('root', views.root, name='root'),

    path('specs', views.specs, name="specs")

]
