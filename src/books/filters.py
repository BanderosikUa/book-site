from django_filters import rest_framework as filters

from .models import Book, AGE_CATEGORY

def filter_by_avg_rating(qs, name, value):
    return qs.filter(avg_rating__gte=value)

def filter_by_genre(qs, name, value):
    return qs.filter(genre__name__in=[value])

def sorting_method(qs, name, sorting):
    if sorting == 1:
        qs = qs.order_by('-time_created')
    elif sorting == 2:
        qs = qs.order_by('-avg_rating')
    elif sorting == 3:
        qs = qs.order_by('-hit_count_generic__hits')
    
    return qs
    

class BaseBookFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    from_date = filters.DateTimeFilter(field_name="time_created", lookup_expr="gte")
    to_date = filters.DateTimeFilter(field_name="time_created", lookup_expr="lte")
    author = filters.CharFilter(
        field_name="author__name",
        lookup_expr="exact"
    )
    views = filters.NumberFilter(field_name='hit_count_generic__hits', lookup_expr='gte')
    # sorting = filters.ChoiceFilter(choices=[1, 2, 3])
    age_category = filters.ChoiceFilter(choices=AGE_CATEGORY)
    rating = filters.NumberFilter(method=filter_by_avg_rating)
    genre = filters.CharFilter(method=filter_by_genre)
    
    class Meta:
        model = Book
        fields = ['time_created', 'author', 'views',
                  'age_category', 'name']
        
    # @property
    # def qs(self):
    #     parent = super().qs
    #     sorting = getattr(self.request, 'sorting', None)
    #     if sorting == 1:
    #         parent = parent.order_by('-time_created')
    #     elif sorting == 2:
    #         parent = parent.order_by('-avg_rating')
    #     elif sorting == 3:
    #         parent = parent.order_by('-hit_count_generic__hits')
    
    #     return parent
