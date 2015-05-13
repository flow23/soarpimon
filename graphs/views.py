from os.path import join

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.conf import settings

from .models import Graph

# THIS IS WHERE THE MAGIC HAPPENS

def index(request):
    graphList = Graph.objects.all()
    #graph_list = Graph.solarObjects.all()
    #categories = Graph._meta.get_field('category').choices
    context = {'graphList': graphList}
    return render(request, 'graphs/index.html', context)

def category(request, category):
    if (category == 'battery'):
        graphList = Graph.batteryObjects.order_by('timePeriod')
    elif (category == 'solar'):
        graphList = Graph.solarObjects.order_by('timePeriod')
    else:
        graphList = Graph.objects.filter(category=category).order_by('timePeriod')

    context = {'graphList': graphList}
    return render(request, 'graphs/category.html', context)

def detail(request, graph_id):
    graph = get_object_or_404(Graph, pk=graph_id)
    return render(request, 'graphs/detail.html', {'graph': graph})

def image(request, graph_id):
    graph = get_object_or_404(Graph, pk=graph_id)
    #imageData = open('/webapp/solar/solar/solar/media/solar-ampere-compare-hour.png', 'rb').read()
    #path = join(os.path.dirname(__file__),  graph.imageFilename.url)
    graph.generateComparisonGraph()
    graphImage = graph.imageFilename.read()
    return HttpResponse(graphImage, content_type='image/png')

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def status(request):
    return HttpResponse("KUUUUURAAAAAHEEEEE")
