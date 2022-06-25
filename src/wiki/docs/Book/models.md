# Book models
## Done
- name
- slug
- about
- photo
- author
- genre
- hitcount
- time_created
- time_modified
- readers
- comments

## To make
- age_category
- collections


# UserBookRelation
Your own ManyToMany implementation of User and Book. This model responsible for rating, liking, bookmarking Book model.
- user
- book
- bookmark(int choices). 1-planning, 2-reading, 3-read, 4-abandoned
- rate(choices from 1 to 5)
