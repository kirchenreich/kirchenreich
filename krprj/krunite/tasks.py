from celery import task

from .models import KircheUnite


@task
def unite_osm(osm):
    """ run like this (in a manage-shell):
from krprj.osm.models import KircheOsm
from krprj.krunite.tasks import unite_osm
[unite_osm(i) for i in KircheOsm.objects.all()]
    """
    unites = KircheUnite.objects.get_by_osm_or_create(osm)
    for unite in unites:
        unite.update_country()
        unite.update_wikipedia()
        unite.update_checks()

    return True
