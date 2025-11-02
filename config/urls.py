from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('debate/', include('apps.debate.urls')), 
    path('', include('apps.feed.urls')),
]