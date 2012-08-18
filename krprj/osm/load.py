# -*- coding: utf-8 -*-
from models import KircheOsm
import codecs
import json

def load_nodes(filename):
    """ imports the churches which are only consisting of one point.
    """
    fp = codecs.open(filename, encoding='utf-8', mode='r')
    for line in fp:
        data = json.loads(line)
        new_kosm, created = KircheOsm.objects.get_or_create(lon=data['refs'][0],
                                                            lat=data['refs'][1],
                                                            osm_id=data['id'])
        if not created:
            continue
        dtags = data.get('tags')
        if 'name' in dtags:
            new_kosm.name = dtags['name']
            del dtags['name']
        if 'religion' in dtags:
            new_kosm.religion = dtags['religion']
            del dtags['religion']
        if 'denomination' in dtags:
            new_kosm.denomination = dtags['denomination']
            del dtags['denomination']
        del dtags['amenity']
        new_kosm.addional_fields = dtags
        new_kosm.save()


def load_polygon(filename):
    """ imports the churches which are consisting of polygons.
    """
    pass
