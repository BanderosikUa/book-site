from django.urls import path, include

from .views import *

urlpatterns = [
    path('author/all/', AuthorAllView.as_view(), name='all-authors'),
    path('author/<slug:author_slug>/', AuthorView.as_view(), name='author'),
]
