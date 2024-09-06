from ..models import Book
from ..selectors import get_users_bookmarks_and_rating

from ..filters import BaseBookFilter

def list_books(*, filters=None):
    filters = filters or {}
    
    qs = (get_users_bookmarks_and_rating()
          .select_related('author')
          .prefetch_related('genre', 'comments', 'hit_count_generic'))
      
    qs = BaseBookFilter(filters, qs).qs
    if "sorting" in filters:
        sorting = filters['sorting']

        if sorting == 1:
            # novelties
            qs = qs.order_by('-time_created')
        elif sorting == 2:
            # popular
            qs = qs.order_by('-hit_count_generic__hits')
        elif sorting == 3:
            # rated
            qs = qs.order_by('-avg_rating')
        
    return qs
