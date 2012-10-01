from django.contrib.gis import admin

from krprj.krunite.tasks import unite_osm_list
from models import KircheOsm


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

    actions = ['update_unite']

    def update_unite(self, request, queryset):
        unite_osm_list.delay(queryset)
        self.message_user(request, "Started %s tasks." % queryset.count())
    update_unite.short_description = "Update selected osm -> unite objects"

admin.site.register(KircheOsm, KircheOsmAdmin)
