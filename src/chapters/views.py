from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.list import ListView

from .models import BookNotification, Chapter
from .service import *

class ChaptersListView(ListView):
    template_name = 'chapters/chapter_page.html'
    paginate_by = 1
    context_object_name = 'chapter'

    def get_queryset(self):
        slug = self.kwargs.get('book_slug')
        return Chapter.objects.filter(book__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        # context['page'] = self.request.GET.get('page')

        return context


def add_notification_to_navbar_view(request):
    user = request.user
    response = add_notification_to_navbar(user)
    return JsonResponse(response)


def delete_notification(request, notification_pk):
    user = request.user
    notification = BookNotification.objects.get(pk=notification_pk)
    if notification.user == user:
        notification.delete()
        return JsonResponse({'deleted': True})
    return JsonResponse({'deleted': False})
