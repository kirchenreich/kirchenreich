from django.contrib.gis import admin
from models import KircheOsm, Ref


class KircheOsmAdmin(admin.OSMGeoAdmin):
    list_display = ['id', 'osm_id', 'name', 'religion', 'denomination', 'lon',
                    'lat', 'osm_type']
    list_filter = ['religion', 'denomination']
    search_fields = ['name', 'osm_id']

    readonly_fields = ['id', 'osm_id', 'osm_type']
    fieldsets = (
        (None, {
            'fields': ('id', 'osm_id', 'osm_type')
        }),
        ('Place informations', {
            'fields': ('name', 'religion', 'denomination', 'addional_fields')
        }),
        ('Geo informations', {
                'fields': ('lon', 'lat', 'point', 'mpoly')
        }),
    )

admin.site.register(KircheOsm, KircheOsmAdmin)


class RefAdmin(admin.OSMGeoAdmin):
    fields = ('osm_id', 'need_update', 'last_update', 'created')
    readonly_fields = ('last_update', 'created')

admin.site.register(Ref, RefAdmin)
