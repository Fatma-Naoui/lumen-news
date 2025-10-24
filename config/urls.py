from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('debate/', include('apps.debate.urls')),  # ✅ Make sure this is here

]