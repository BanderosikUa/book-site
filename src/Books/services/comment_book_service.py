from django.contrib.auth.models import User
from ..models import CommentBook
from ..selectors import CommentBookSelector

def get_comment_data(*, book_pk: int, num_comments: int, user: User) -> dict:
    """Function, that return Json with limited(3) data of comments in GET ajax request"""
    visible = 3
    upper = num_comments
    lower = upper - visible
    selector = CommentBookSelector(book_pk=book_pk)
    qs = selector.comment.order_by('time_created')
    size = qs.count()
    data = []
    for obj in qs:
        item = {
            'pk': obj.pk,
            'username': obj.user.username,
            'avatar': obj.user.avatar.url,
            'comment': obj.body,
            'likes': obj.comment_likes,
            'dislikes': obj.comment_dislikes,
            'time_created': obj.time_created.strftime("%d %B %Y"),
            'liked': True if user in obj.liked.all() else False,
            'disliked': True if user in obj.disliked.all() else False,
        }
        data.append(item)
    return {'data': data[lower:upper], 'size': size}


def like_book_comment(*, comment_pk: int, book_pk: int, user: User):
    """Function, that add or remove user like to book's comment"""
    comment = CommentBookSelector(book_pk=book_pk, comment_pk=comment_pk)
    disliked = False
    if comment.users_likes_filter_by_username(username=user.username).exists():
        comment.user_likes.remove(user)
        liked = False
    elif comment.users_dislikes_filter_by_username(username=user.username).exists():
        comment.user_dislikes.remove(user)
        comment.user_likes.add(user)
        liked = True
    else:
        comment.user_likes.add(user)
        liked = True
    return {'likes': comment.likes_amount,
            'dislikes': comment.dislikes_amount,
            'liked': liked,
            'disliked': disliked}


def dislike_book_comment(comment_pk: int, book_pk: int, user: User) -> dict:
    """Function, that add or remove user dislike to book's comment"""
    comment = CommentBookSelector(book_pk=book_pk, comment_pk=comment_pk)
    username = user.username
    liked = False
    if comment.users_dislikes_filter_by_username(username=username).exists():
        comment.user_dislikes.remove(user)
        disliked = False
    elif comment.users_likes_filter_by_username(username=username).exists():
        comment.user_likes.remove(user)
        comment.user_dislikes.add(user)
        disliked = True
    else:
        comment.user_dislikes.add(user)
        disliked = True
        
    return {'dislikes': comment.dislikes_amount,
            'likes': comment.likes_amount,
            'liked': liked,
            'disliked': disliked}


def create_comment(*, book_pk: int, body: str, user: User) -> dict:
    """Function, that create comment model from AJAX post request"""
    response_data = dict()
    UserComment = CommentBook.objects.create(
        book_id=book_pk,
        user=user,
        body=body
    )
    response_data['username'] = user.username
    response_data['comment'] = body
    response_data['pk'] = UserComment.pk
    response_data['time_created'] = UserComment.time_created.strftime("%d %B %Y")
    response_data['likes'] = 0
    response_data['dislikes'] = 0
    response_data['avatar'] = user.avatar.url
    response_data['pk'] = user.pk

    return response_data
