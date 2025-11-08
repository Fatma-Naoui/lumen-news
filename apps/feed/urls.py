from django.urls import path
from . import views

app_name = 'feed'  

urlpatterns = [
    path('', views.index, name='index'),
    path('feed/', views.feed, name='feed'),
    path('contact/', views.contact, name='contact'),
]