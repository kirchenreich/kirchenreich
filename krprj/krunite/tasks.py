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


@task
def unite_osm_list(osm_list):
    for osm_obj in osm_list:
        unite_osm.delay(osm_obj)
    return len(osm_list)


@task
def update_checks(unite):
    unite.update_checks()
    return True


@task
def update_checks_list(unite_list):
    for unite in unite_list:
        update_checks.delay(unite)
    return len(unite_list)


@task
def update_unite(unite):
    unite.update()
    return True


@task
def update_unite_list(unite_list):
    for unite in unite_list:
        update_unite.delay(unite)
    return len(unite_list)
