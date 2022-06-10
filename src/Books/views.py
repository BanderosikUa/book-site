from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.db.models import Avg, Count, Q, Sum


from hitcount.views import HitCountDetailView


from Books.services import *
from Books.selectors import *
from Books.forms import CommentCreateForm
from .models import Book, UserBookRelation, CommentBook



class BookView(HitCountDetailView):
    """Class-based view for displaying Book and UserBookRelation models"""
    model = Book
    template_name = "Books/main.html"
    slug_url_kwarg = 'book_slug'
    count_hit = True

    def get_object(self, queryset=None):
        slug = self.kwargs.get('book_slug')
        book = get_users_bookmarks_and_rating()
        return get_object_or_404(book
                                 .select_related('author')
                                 .prefetch_related('genre'),
                                 slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = context['object']

        create_comment_form = CommentCreateForm()
        if self.request.user.is_authenticated:
            user_relation = get_book_relation(book=book).get_or_create(user=self.request.user, book=book)
            context['user_relation'] = user_relation[0]
        context['Book'] = book
        context['comment_create_form'] = create_comment_form
        return context


def test(request):
    return render(request, 'Books/main.html')


def get_average_rating_view(request, book_pk):
    response = get_average_rating(book_pk=book_pk)
    return JsonResponse({'avg_rating': response})


def rate_book_view(request):
    book_pk = request.POST.get('pk')
    rate_value = request.POST.get('value')
    user = request.user
    create_rate_book(book_pk=book_pk, rate=rate_value, user=user)
    return JsonResponse({'status': 'success'})


def get_comment_data_view(request, book_pk, num_comments):
    """Function, that return Json with limited(3) data of comments in GET ajax request"""
    user = request.user
    response = get_comment_data(book_pk=book_pk,
                                num_comments=num_comments,
                                user=user
                                )
    return JsonResponse(response)


def like_book_comment_view(request):
    """Function, that add or remove user like to book's comment
    and return Json in POST ajax request"""
    comment_pk = request.POST.get('comment_pk')
    book_pk = request.POST.get('book_pk')
    user = request.user

    response = like_book_comment(comment_pk=comment_pk, 
                                 book_pk=book_pk,
                                 user=user)
    print(response)
    return JsonResponse(response)


def dislike_book_comment_view(request):
    """Function, that add or remove user dislike to book's comment
    and return Json in POST ajax request"""
    comment_pk = request.POST.get('comment_pk')
    book_pk = request.POST.get('book_pk')
    user = request.user

    response = dislike_book_comment(comment_pk=comment_pk, 
                                    book_pk=book_pk,
                                    user=user)
    
    return JsonResponse(response)


def create_comment_view(request):
    """Function, that create comment model from AJAX post request"""
    user = request.user
    book_pk = request.POST.get('book_pk')
    body = request.POST.get('comment')
    
    response = create_comment(book_pk=book_pk, body=body, user=user)
    
    return JsonResponse(response)


def bookmark_book_view(request):
    """Function, that add or remove user bookmark and return selected bookmark"""
    book_pk = request.POST.get('book_pk')
    bookmark = int(request.POST.get('bookmarked'))
    user = request.user

    response = bookmark_book(book_pk=book_pk, bookmark=bookmark, user=user)

    return JsonResponse(response)

def get_bookmark_data_view(request, book_pk):
    """Function, that return selected user bookmark"""
    response = get_bookmark_data(book_pk=book_pk, user=request.user)
    return JsonResponse(response)
