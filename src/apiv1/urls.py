from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'book', BookViewSet)
print(router.urls)

urlpatterns = [
    path('', include(router.urls)),
]
