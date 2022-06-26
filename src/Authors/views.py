from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

from hitcount.views import HitCountDetailView

from .models import Author


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

# def test(request, author_slug):
#     return HttpResponse('asdasd')


# Create your views here.
