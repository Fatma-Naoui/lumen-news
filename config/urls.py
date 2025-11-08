from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.chatbot.urls")),
    path("debate/", include("apps.debate.urls")),
      # Add this if you have scraper urls
    
    # Commented out - not integrated yet
    # path("sentiment/", include("apps.sentiment.urls")),
    # path("users/", include("apps.users.urls")),
    # path("recommendations/", include("apps.recommendations.urls")),
    # path("feed/", include("apps.feed.urls")),
    # path("speech/", include("apps.speech.urls")),
]