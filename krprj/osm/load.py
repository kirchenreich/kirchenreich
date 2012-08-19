# -*- coding: utf-8 -*-
from models import KircheOsm
import codecs
import json
from django.contrib.gis.geos import MultiPolygon, Polygon

def load_nodes(filename):
    """ imports the churches which are only consisting of one point.
    """
    fp = codecs.open(filename, encoding='utf-8', mode='r')
    for line in fp:
        data = json.loads(line)

        kosm, created = KircheOsm.objects.get_or_create(osm_id=data['id'])

        kosm.lon = data['refs'][0]
        kosm.lat = data['refs'][1]

        dtags = data.get('tags')
        if 'name' in dtags:
            kosm.name = dtags['name']
            del dtags['name']
        if 'religion' in dtags:
            kosm.religion = dtags['religion']
            del dtags['religion']
        if 'denomination' in dtags:
            kosm.denomination = dtags['denomination']
            del dtags['denomination']
        del dtags['amenity']
        kosm.addional_fields = json.dumps(dtags)

        # set mpoly and point in dataset
        kosm.set_geo()
        kosm.save()


def load_polygon(filename):
    """ imports the churches which are consisting of polygons.
    """
    # read all coordinates in memory
    fp = codecs.open('krprj/osm/data/coords_merged.data', encoding='utf-8', mode='r')
    coords = {}
    for line in fp:
        try:
            d = json.loads(line)
            coords[d.get('id')] = d
        except:
            print line
    fp.close()
    print("dict loaded")
    fp = codecs.open('krprj/osm/data/ways.data', encoding='utf-8', mode='r')
    for line in fp:
        data = json.loads(line)

        kosm, created = KircheOsm.objects.get_or_create(osm_id=data['id'])

        dtags = data.get('tags')
        if 'name' in dtags:
            kosm.name = dtags['name']
            del dtags['name']
        if 'religion' in dtags:
            kosm.religion = dtags['religion']
            del dtags['religion']
        if 'denomination' in dtags:
            kosm.denomination = dtags['denomination']
            del dtags['denomination']
        del dtags['amenity']
        kosm.addional_fields = json.dumps(dtags)

        tpl = []
        for ref in data.get('refs'):
            x = coords.get(ref)
            if x:
                tpl.append(tuple([x.get('lon'), 
                                  x.get('lat')]))
            else:
                print("missing: %d" % ref)

        kosm.mpoly = MultiPolygon(Polygon(tuple(tpl)))
        print kosm.mpoly

        kosm.point = kosm.mpoly.centroid
        print kosm.point

        kosm.save()
