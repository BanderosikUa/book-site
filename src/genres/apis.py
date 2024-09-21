from rest_framework import serializers
from rest_framework.views import Response, APIView

from cacheops import cached

from api.pagination import LimitOffsetPagination, get_paginated_response

from .models import Genre


class GenresNameListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 100
    
    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        url = serializers.URLField(source='get_absolute_url')

    def get(self, request):
        
        genres = Genre.objects.order_by('hit_count_generic__hits').all().cache()
                
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=genres,
            request=request,
            view=self
        )
