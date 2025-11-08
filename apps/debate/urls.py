from django.urls import path
from . import views

urlpatterns = [
       path('', views.debate_page, name='debate_page'),
    path('stream/', views.stream_debate, name='stream_debate'),
]
