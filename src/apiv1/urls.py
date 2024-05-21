from django.urls import path, include
from rest_framework import routers

from .views import *
from .views.comment_viewsets import CommentBookViewSet

app_name = 'apiv1'

router = routers.SimpleRouter()
router.register(r'book', BookViewSet)
router.register(r'comment', CommentBookViewSet, basename='comment')
print(router.urls)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # path('comment/<int:book_pk>/', CommentBookViewSet.as_view({'get': 'list'}))
]
