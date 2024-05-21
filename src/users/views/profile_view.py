from django.http import JsonResponse
from django.views.generic import DetailView

from ..services import get_user_comments_data

from ..models import CustomUser


class ProfileView(DetailView):
    model = CustomUser
    context_object_name = 'profile_user'
    slug_url_kwarg = 'user_slug'
    template_name = 'users/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        user = context['profile_user']

        context['books_reading'] = (
            user.books
            .filter(userbookrelation__bookmarks=2)
            )

        return context


def get_user_comments_view(request, user_slug, num_comments):
    user = CustomUser.objects.get(slug=user_slug)
    response = get_user_comments_data(user=user,
                                      num_comments=num_comments)
    return JsonResponse(response)
