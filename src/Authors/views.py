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

    # def get_object(self):
    #     slug = self.kwargs.get('author_slug')
    #     print('ok')
    #     return Author.objects.get(slug=slug)

# def test(request, author_slug):
#     return HttpResponse('asdasd')


# Create your views here.
