from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

class SystemStatusView(TemplateView):
    template_name = "ss.html"

# def index(request):
#     return HttpResponse("You're looking at")

