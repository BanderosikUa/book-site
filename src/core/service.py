# from django.db.models import QuerySet


# def make_carousels_list(
#     *,
#     books_novelties_qs: QuerySet,
#     popular_books_qs: QuerySet,
#     popular_authors_qs: QuerySet
#         ) -> list[dict]:
    
#     books_novelties = {
#         'name': 'New books!',
#         'ordering': books_novelties_qs
#         }
#     popular_books = {
#         'name': "Popular books!",
#         'ordering': popular_books_qs
#         }
#     popular_authors = {
#         'name': 'Popular authors!',
#         'ordering': popular_authors_qs
#         }
#     carousels = [
#         books_novelties,
#         popular_books,
#         popular_authors
#     ]
#     return carousels
