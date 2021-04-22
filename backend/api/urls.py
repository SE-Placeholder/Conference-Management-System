from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from api import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('auth', include('authentication.urls')),
    path('dummy', include('dummy.urls')),

    path('conferences', include('conference.urls')),
    path('papers', include('paper.urls')),

    path('user', include('role.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
