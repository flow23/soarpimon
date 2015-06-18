from django.contrib import admin

from .models import Graph

class GraphAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Meta',               {'fields': ['description', 'category', 'displayOnStatusPage', 'rrdFilename', 'imageFilename'], 'classes': ['collapse']}),
        ('Graphing',           {'fields': ['timePeriod', 'end', 'unit', 'verticalLabel', 'watermark', 'width', 'height', 'upperLimit', 'lowerLimit', 'lowerLimitRigid', 'lineColor', 'areaColor']}),
        ('Date information',   {'fields': ['generationDate'], 'classes': ['collapse']}),
    ]
    list_display = ('description', 'imageFilename', 'lastChange', 'generationDate')
    list_filter = ['lastChange', 'generationDate']
    search_fields = ['description']

admin.site.register(Graph, GraphAdmin)
