from django.contrib.gis import admin

from krprj.osm.models import KircheOsm
from .models import KircheChecks, KircheUnite
from .tasks import update_checks_list, update_unite_list


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
        })
        # This is not very helpful because there is no point/mpoly
        # edit widget for inlines.
        # ('Geo informations', {
        #         'fields': ('lon', 'lat', 'point', 'mpoly')
        # }),
    )


class ChecksInline(admin.StackedInline):
    model = KircheChecks
    max_num = 1


class UniteAdmin(admin.OSMGeoAdmin):
    list_display = ['id', 'name', 'religion', 'denomination', 'country',
                    'last_update', 'created']
    readonly_fields = ['last_update', 'created']
    fieldsets = (
        (None, {
            'fields': ('name', 'religion', 'denomination', 'point',
                       'country', 'last_update', 'created')
        }),
    )
    inlines = [OSMInline]

    actions = ['update_unite', 'update_checks']

    def update_unite(self, request, queryset):
        update_unite_list.delay(queryset)
        self.message_user(request, "Started %s tasks." % queryset.count())
    update_unite.short_description = "Update the unite object of selection"

    def update_checks(self, request, queryset):
        update_checks_list.delay(queryset)
        self.message_user(request, "Started %s tasks." % queryset.count())
    update_checks.short_description = "Update checks of selection"

admin.site.register(KircheUnite, UniteAdmin)


class KircheChecksAdmin(admin.OSMGeoAdmin):
    list_display = ['id', 'kircheunite', 'last_update', 'created']

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
