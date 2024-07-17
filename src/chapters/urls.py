from django.urls import path
from .views import *


urlpatterns = [
    path('book/<slug:book_slug>/read/', ChaptersListView.as_view(), name='book-chapters'),
    path('get-notifications/', add_notification_to_navbar_view, name='get-notifications'),
    path('delete-notification/<int:notification_pk>/', delete_notification, name='delete-notification'),
]
