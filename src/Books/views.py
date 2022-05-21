from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView
from .models import Book, UserBookRelation
from .forms import RateForm


class BookView(UpdateView):
    model = Book
    template_name = "Books/main.html"
    slug_url_kwarg = 'book_slug'
    form_class = RateForm
    # context_object_name = 'Book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('book_slug')
        context['Book'] = get_object_or_404(Book, slug=slug)
        return context

    def form_valid(self, form):
        print('ok')
        return super().form_valid(form)


def test(request):
    return render(request, 'Books/main.html')


# Create your views here.
