from django.contrib import admin

from .models import Graph

class GraphAdmin(admin.ModelAdmin):
    #fieldsets = [
    #    (None,               {'fields': ['description']}),
    #    ('Date information', {'fields': ['generationDate'], 'classes': ['collapse']}),
    #]
    list_display = ('description', 'imageFilename', 'lastChange', 'generationDate')
    list_filter = ['lastChange', 'generationDate']
    search_fields = ['description']

admin.site.register(Graph, GraphAdmin)
