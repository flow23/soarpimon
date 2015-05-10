from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from solar import views
from graphs import views as graphs_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'solar.views.home', name='home'),
    url(r'^$', views.IndexView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^$', 'views.index', name='index'),
    url(r'^polls/', include('polls.urls')),
    url(r'^system-status/', include('abcdef.urls')),
    url(r'^graphs/', include('graphs.urls')),
    url(r'^system-status/', graphs_views.systemstatus, name='systemstatus'),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
