from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /graphs/
    url(r'^$', views.index, name='index'),
    # ex: /graphs/5/
    url(r'^(?P<graph_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /graphs/category/solar|battery/
    url(r'^category/(?P<category>\w+)/$', views.category, name='category'),
    # ex: /graphs/image/1/
    url(r'^image/(?P<graph_id>[0-9]+)/$', views.image, name='image'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
