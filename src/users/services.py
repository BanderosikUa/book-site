from django.contrib.auth.models import User

from books.models import CommentBook


def get_user_comments_data(*, num_comments: int, user: User) -> dict:
    """Function, that return Json with limited(10) data of comments in GET ajax request"""
    visible = 10
    upper = num_comments
    lower = upper - visible
    qs = (
        CommentBook.objects
        .filter(user=user)
        .order_by('-time_created')
    )
    size = qs.count()
    data = []
    for obj in qs:
        item = {
            'pk': obj.pk,
            'username': obj.user.username,
            'avatar': obj.user.avatar.url,
            'book_photo': obj.book.photo.url,
            'book_url': obj.book.get_absolute_url(),
            'user_url': obj.user.get_absolute_url(),
            'comment': obj.body,
            'likes': obj.comment_likes,
            'dislikes': obj.comment_dislikes,
            'time_created': obj.time_created.strftime("%d %B %Y"),
        }
        data.append(item)
    return {'data': data[lower:upper], 'size': size}
