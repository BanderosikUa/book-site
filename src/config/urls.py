from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('core.urls')),
    path('', include('Chapters.urls')),
    path('', include('Books.urls')),
    path('', include('Genres.urls')),
    path('', include('users.urls')),
    path('', include('Authors.urls'))
]

if settings.local.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.base.MEDIA_URL,
                          document_root=settings.base.MEDIA_ROOT)
