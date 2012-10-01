from celery import task
from imposm.parser import OSMParser
import json
import os.path
import sys

from .models import KircheOsm

@task
def insert_church_node(data):
    # write updates ids for debugging
    fp = open('/tmp/foo.log', 'a')
    fp.write('%s\n' % data['id'])
    fp.close()
    ##
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
    kosm.osm_type = 'N'

    # set mpoly and point in dataset
    kosm.set_geo()
    kosm.save()

@task
def insert_refs_needed(refs):
    pass

@task
def insert_church_way(data):
    pass

class GetChurches(object):
    """ collect all nodes and ways with amenity="place_of_worship"
    """

    def nodes(self, nodes):
        """ create for every place_of_worship node a task 
        """
        for osmid, tags, refs in nodes:
            if 'amenity' in tags and tags.get('amenity') == 'place_of_worship':
                d = {'id': osmid, 'tags': tags, 'refs': refs}
                ## add task to celery
                insert_church_node.apply_async(args=[d])

    def ways(self, ways):
        """ create for every place_of_worship way a task 
        """
        for osmid, tags, refs in ways:
            if 'amenity' in tags and tags.get('amenity') == 'place_of_worship':
                d = {'id': osmid, 'tags': tags, 'refs': refs}
                ## add task to celery -- add refs needed for ways
                insert_refs_needed.apply_async(args=[refs])
                ## add task to celery -- insert way / execute later (1h)
                insert_church_way.apply_async(args=[d], countdown=3600)

@task
def add_churches(filename):
    first = GetChurches()
    p = OSMParser(concurrency=4,
                  nodes_callback=first.nodes)
#                  ways_callback=first.ways)
    p.parse(filename)

    # TODO: fill all refs missing in database 

    return True

