from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.urls import include
from django.urls import re_path as url
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('donutapp.urls')),
    url(r'^', include('donutapp.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)