from django.conf import settings
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Author
from .service import get_tops_dict


class AuthorView(DetailView):
    model = Author
    template_name = 'authors/author_page.html'
    count_hit = True
    slug_url_kwarg = 'author_slug'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['genres'] = (context['author']
                             .books
                             .values('genre__name', 'genre__slug')
                             .distinct()
                             )
        
        return context


class AuthorAllView(ListView):
    template_name = 'authors/all_author_page.html'
    context_object_name = 'authors'

    def get_queryset(self):
        authors = (
            Author.objects
            .all()
            .prefetch_related('books')
        )
        return authors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request.COOKIES.get(settings.SESSION_COOKIE_NAME))
        context['tops'] = get_tops_dict(self.object_list)
        
        return context
