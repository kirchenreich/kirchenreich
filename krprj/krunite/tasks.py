from celery import task

from .models import KircheUnite


@task
def unite_osm(osm):
    unites = KircheUnite.objects.get_by_osm_or_create(osm)
    for unite in unites:
        unite.update_country()
        unite.update_wikipedia()
        unite.update_checks()

    return True
