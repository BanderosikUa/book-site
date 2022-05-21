from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Books.urls')),
]

if settings.local.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.base.MEDIA_URL,
                          document_root=settings.base.MEDIA_ROOT)
