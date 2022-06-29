from django.views.generic.list import ListView


from hitcount.views import HitCountDetailView

from .models import Author
from .service import get_tops_dict

class AuthorView(HitCountDetailView):
    template_name = 'Authors/author_page.html'
    count_hit = True
    slug_url_kwarg = 'author_slug'
    model = Author
    context_object_name = 'author'

    # def get_object(self):
    #     author = super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['genres'] = (context['author']
                             .book_author
                             .values('genre__name', 'genre__slug')
                             .distinct()
                             )
        
        return context

class AuthorAllView(ListView):
    template_name = 'Authors/all_author_page.html'
    context_object_name = 'authors'

    def get_queryset(self):
        authors = (
            Author.objects
            .all()
            .prefetch_related('book_author')
        )
        return authors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tops'] = get_tops_dict(self.object_list)
        
        return context
