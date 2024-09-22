from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from hitcount.views import HitCountJSONView

from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path('hit/ajax/', HitCountJSONView.as_view(), name='hit_ajax'),
    path('api/v1/', include('api.urls')),
    path('', include('core.urls')),
    path('', include('chapters.urls')),
    path('', include('books.urls')),
    path('', include('genres.urls')),
    path('', include('users.urls')),
    path('', include('authors.urls'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += [
        path('silk/', include('silk.urls', namespace='silk'))
    ]
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
