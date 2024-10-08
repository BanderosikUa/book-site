from django.views.generic import DetailView

from ..models import User


class ProfileView(DetailView):
    model = User
    context_object_name = 'profile_user'
    slug_url_kwarg = 'user_slug'
    template_name = 'users/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        user = context['profile_user']

        context['books_reading'] = (
            user.bookrelations
            .filter(bookmarks=2)
            )
        return context
