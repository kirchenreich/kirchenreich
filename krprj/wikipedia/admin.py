from django.contrib.gis import admin
from models import KircheWikipedia

class KircheWikipediaAdmin(admin.OSMGeoAdmin):
    list_display = ['id', 'title', 'lon', 'lat', 'unite']
    search_fields = ['title']

    readonly_fields = ['id']

admin.site.register(KircheWikipedia, KircheWikipediaAdmin)
