from django.urls import path, include
from rest_framework import routers

app_name = 'apiv1'

router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
