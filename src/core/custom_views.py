from django.views.generic.list import ListView

from hitcount.views import DetailView, HitCountMixin
from hitcount.models import HitCount


class HitCountListView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hit_count = HitCount.objects.get_for_object(kwargs.get('hitcount_object'))
        hits = hit_count.hits
        hit_count_response = HitCountMixin.hit_count(self.request, hit_count)
        context['hitcount'] = {'pk': hit_count.pk}
        context['hitcount']['hit_counted'] = hit_count_response.hit_counted
        context['hitcount']['total_hits'] = hits
        return context        
