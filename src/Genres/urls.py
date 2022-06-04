from django.urls import path
from .views import GenreDetailView

urlpatterns = [
    path('genres/<slug:genre_slug>/', GenreDetailView.as_view(), name='genres'),
]
