# Book models
## Done
- name
- slug
- about
- photo
- author
- genre
- count_views
- time_created
- time_modified
- readers
-

## To make
- age_category
- comments
- collections


# UserBookRelation
Your own ManyToMany implementation of User and Book. This model responsible for rating, liking, bookmarking Book model.
-user
-book
-like(bool)
-in_bookmarks(bool)
-rate(choices)
