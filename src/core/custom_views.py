import warnings
from collections import namedtuple

from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.generic import View, DetailView

from hitcount.utils import get_ip
from hitcount.models import Hit, BlacklistIP, BlacklistUserAgent
from hitcount.utils import RemovedInHitCount13Warning, get_hitcount_model


from hitcount.views import DetailView, HitCountMixin
from django.views.generic.list import ListView

class HitCountDetailView(ListView, HitCountMixin):
    """
    HitCountDetailView provides an inherited DetailView that will inject the
    template context with a `hitcount` variable giving you the number of
    Hits for an object without using a template tag.
    Optionally, by setting `count_hit = True` you can also do the business of
    counting the Hit for this object (in lieu of using JavaScript).  It will
    then further inject the response from the attempt to count the Hit into
    the template context.
    """
    count_hit = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            hit_count = get_hitcount_model().objects.get_for_object(self.object)
            hits = hit_count.hits
            context['hitcount'] = {'pk': hit_count.pk}

            if self.count_hit:
                hit_count_response = self.hit_count(self.request, hit_count)
                if hit_count_response.hit_counted:
                    hits = hits + 1
                context['hitcount']['hit_counted'] = hit_count_response.hit_counted
                context['hitcount']['hit_message'] = hit_count_response.hit_message

            context['hitcount']['total_hits'] = hits

        return context
