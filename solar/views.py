from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView, ListView

from graphs.models import Graph

class IndexView(TemplateView):
    template_name = "index.html"

class StatusView(ListView):
    template_name = "status.html"
    model = Graph
    queryset = Graph.statusObjects.all()

    def get_context_data(self, **kwargs):
        context = super(StatusView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

#def status(request):
#    graphList = get_list_or_404(Graph, pk=1,3,5,7,9)
#    return render(request, 'solar/status.html', {'graphList': graphList})

# def index(request):
#     return HttpResponse("You're looking at")

