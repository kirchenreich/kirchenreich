from django.contrib.gis import admin
from models import KircheOsm

admin.site.register(KircheOsm, admin.OSMGeoAdmin)
