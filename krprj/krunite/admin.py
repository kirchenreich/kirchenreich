from django.contrib.gis import admin
from .models import KircheChecks


class KircheChecksAdmin(admin.OSMGeoAdmin):
    list_display = ['id', 'last_update', 'created', 'kircheunite']

    list_display += KircheChecks().available

    readonly_fields = list_display
    fieldsets = (
        (None, {
            'fields': ('id', 'last_update', 'created')
        }),
        ('Checks', {
            'fields': tuple(KircheChecks().available)
        }),
    )


admin.site.register(KircheChecks, KircheChecksAdmin)
