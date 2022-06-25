# Architecture of the site(tips)
## Static
Save all of your separated for specific app static files(like js scripts, images etc) in other_static/name_of_app
## Templates
Save majority of your templates for specific app in your_app/templates/name_of_your_app. Save only main templates(like a navbar, base.html with imports or footer) in global /templates/ folder.
## Media
Set to your model field(img field, upload_to argument) to save images file only in up `general_name_of_files/%Y/%m/%d/`
## Services
All of your business logic must be located here. For example, function for creating book or delete bookmark.
## View
DON'T write business logic here! Only fetching data, calling services function, preparing to response.
## Selectors
Write here code to fetch data from database.
## Tests
Write here code to test services and selectors functions. Also test url response.
## Models
Write here code only that showing structure of model. Don't write business logic in models. Only coding here some main function like get_absolute_url, `__str__`, etc.
## HitCount(django extension)
This extension is need for counting by ip users view for some model. Create a post_save signal
that will add default hit for model if you want to sorting by "-hit_count_generic__hits" otherwise
it will order incorrect.


