from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_debate, name='test_debate'),
    path('status/<uuid:task_id>/', views.check_debate_status, name='check_debate_status'),
]
