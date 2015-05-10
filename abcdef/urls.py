from django.conf.urls import url

from abcdef import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
]
