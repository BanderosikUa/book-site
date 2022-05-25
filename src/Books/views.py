from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, FormView
from django.db.models import Avg, Count
from .models import Book, UserBookRelation
from .forms import RateForm


class BookView(FormView):
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


def test(request):
    return render(request, 'Books/main.html')


def get_avarage_rating(request, book_pk):
    book = Book.objects.get(pk=1)
    qs_user_book_relations = UserBookRelation.objects.filter(book=book)
    aggregations = qs_user_book_relations.aggregate(Avg('rate'), Count('user'))
    avarage_rating = round(aggregations['rate__avg'], 1)
    return JsonResponse({'avg_rating': avarage_rating,
                         'user_rating_count': aggregations['user__count']})


def rate_book(request):
    book_pk = request.POST.get('pk')
    book = Book.objects.get(pk=book_pk)
    rate_value = request.POST.get('value')
    user = request.user
    try:
        user_book_relation = UserBookRelation.objects.get(book=book, user=user)
        user_book_relation.rate = rate_value
        user_book_relation.save()
    except UserBookRelation.DoesNotExist:
        UserBookRelation.objects.create(book=book, user=user, rate=rate_value)
    return JsonResponse({'ok': True})
