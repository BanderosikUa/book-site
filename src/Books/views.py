from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView
from django.db.models import Avg, Count, Q, Sum

from .models import Book, UserBookRelation
from .forms import RateForm


class BookView(UpdateView):
    """Class-based view for displaying Book and UserBookRelation models"""
    model = Book
    template_name = "Books/main.html"
    slug_url_kwarg = 'book_slug'
    form_class = RateForm
    # context_object_name = 'Book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('book_slug')
        book = get_object_or_404(Book, slug=slug)
        relation = UserBookRelation.objects.filter(book=book)
        user_relation = UserBookRelation.objects.get_or_create(book=book, user=self.request.user)
        context['Book'] = book
        context['users_reviews'] = relation
        context['user_relation'] = user_relation[0]
        context['planning_users'] = relation.filter(bookmarks=1).count()
        context['reading_users'] = relation.filter(bookmarks=2).count()
        context['read_users'] = relation.filter(bookmarks=3).count()
        context['abandonded_users'] = relation.filter(bookmarks=4).count()
        return context


def test(request):
    return render(request, 'Books/main.html')


def get_avarage_rating(request, book_pk):
    """Function, that calculate avarage rating of the book and
    return json into ajax function with GET request"""
    book = Book.objects.get(pk=book_pk)
    qs_user_book_relations = UserBookRelation.objects.filter(book=book)
    if qs_user_book_relations:
        aggregations = qs_user_book_relations.aggregate(Avg('rate'), Count('user'))
        avarage_rating = round(aggregations['rate__avg'], 1)
        return JsonResponse({'avg_rating': avarage_rating,
                            'user_rating_count': aggregations['user__count']})
    else:
        return JsonResponse({'avg_rating': 0})


def rate_book(request):
    """Function, that add user rating into created or updated UserBookRealtion
    model and return json into ajax function with POST request"""
    book_pk = request.POST.get('pk')
    book = Book.objects.get(pk=book_pk)
    rate_value = request.POST.get('value')
    user = request.user
    user_book_relation = UserBookRelation.objects.get(book=book, user=user)
    user_book_relation.rate = rate_value
    user_book_relation.save()
    return JsonResponse({'status': 'success'})

def get_comment_data(request, book_pk, num_comments):
    """Function, that return Json with limited(3) data of comments in GET ajax request"""
    visible = 3
    upper = num_comments
    lower = upper - visible
    book = Book.objects.get(pk=book_pk)
    qs = UserBookRelation.objects.filter(book=book).exclude(comment='').order_by('comment_time_created')
    size = qs.count()
    data = []
    for obj in qs:
        item = {
            'pk': obj.pk,
            'username': obj.user.username,
            'comment': obj.comment,
            'likes': obj.comment_likes,
            'dislikes': obj.comment_dislikes,
            'time_created': obj.comment_time_created.strftime("%d %B %Y"),
            'liked': True if request.user in obj.comment_liked.all() else False,
            'disliked': True if request.user in obj.comment_disliked.all() else False,
        }
        data.append(item)
    return JsonResponse({'data':data[lower:upper],'size': size})

def like_book_comment(request):
    """Function, that add or remove user like to book's comment
    and return Json in POST ajax request"""
    relation_pk = request.POST.get('comment_pk')
    relation = UserBookRelation.objects.get(pk=relation_pk)
    users_that_like_comment = relation.comment_liked
    users_that_dislike_comment = relation.comment_disliked
    disliked = False
    if request.user in users_that_like_comment.all():
        users_that_like_comment.remove(request.user)
        liked = False
    elif request.user in users_that_dislike_comment.all():
        users_that_dislike_comment.remove(request.user)
        users_that_like_comment.add(request.user)
        liked = True
    else:
        users_that_like_comment.add(request.user)
        liked = True
    return JsonResponse({'likes': relation.comment_likes, 
                         'dislikes': relation.comment_dislikes,
                         'liked': liked,
                         'disliked': disliked})

def dislike_book_comment(request):
    """Function, that add or remove user dislike to book's comment
    and return Json in POST ajax request"""
    relation_pk = request.POST.get('comment_pk')
    relation = UserBookRelation.objects.get(pk=relation_pk)
    users_that_dislike_comment = relation.comment_disliked
    users_that_like_comment = relation.comment_liked
    liked = False
    if request.user in users_that_dislike_comment.all():
        users_that_dislike_comment.remove(request.user)
        disliked = False
    elif request.user in users_that_like_comment.all():
        users_that_like_comment.remove(request.user)
        users_that_dislike_comment.add(request.user)
        disliked = True
    else:
        users_that_dislike_comment.add(request.user)
        disliked = True
        
    return JsonResponse({'dislikes': relation.comment_dislikes, 
                         'likes': relation.comment_likes,
                         'liked': liked,
                         'disliked': disliked})
