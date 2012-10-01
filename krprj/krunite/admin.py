from django.contrib.gis import admin

from krprj.osm.models import KircheOsm
from .models import KircheChecks, KircheUnite


class OSMInline(admin.StackedInline):
    model = KircheOsm
    extra = 0

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


class UniteAdmin(admin.OSMGeoAdmin):
    readonly_fields = ['last_update', 'created']
    fieldsets = (
        (None, {
            'fields': ('name', 'point', 'country', 'last_update', 'created')
        }),
    )
    inlines = [OSMInline]

admin.site.register(KircheUnite, UniteAdmin)


# class KircheChecksAdmin(admin.OSMGeoAdmin):
#     list_display = ['id', 'last_update', 'created', 'kircheunite']

#     list_display += KircheChecks().available

#     readonly_fields = list_display
#     fieldsets = (
#         (None, {
#             'fields': ('id', 'last_update', 'created')
#         }),
#         ('Checks', {
#             'fields': tuple(KircheChecks().available)
#         }),
#     )


# admin.site.register(KircheChecks, KircheChecksAdmin)
