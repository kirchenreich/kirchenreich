from django.contrib.gis import admin
from models import KircheOsm


class KircheOsmAdmin(admin.OSMGeoAdmin):
    list_display = ['id', 'osm_id', 'name', 'religion', 'denomination', 'lon',
                    'lat']
    list_filter = ['religion', 'denomination']
    search_fields = ['name', 'osm_id']

    readonly_fields = ['id', 'osm_id']
    fieldsets = (
        (None, {
            'fields': ('id', 'osm_id')
        }),
        ('Place informations', {
            'fields': ('name', 'religion', 'denomination', 'addional_fields')
        }),
        ('Geo informations', {
                'fields': ('lon', 'lat', 'mpoly', 'point')
        }),
    )

admin.site.register(KircheOsm, KircheOsmAdmin)
