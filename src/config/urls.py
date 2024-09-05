from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from django.views.generic import TemplateView

from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('api/v1/', include('apiv1.urls')),
    path('', include('core.urls')),
    path('', include('chapters.urls')),
    path('', include('books.urls')),
    path('', include('genres.urls')),
    path('', include('users.urls')),
    path('', include('authors.urls'))
]

if settings.local.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.base.MEDIA_URL,
                            document_root=settings.base.MEDIA_ROOT)
