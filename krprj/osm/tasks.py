from celery import task
from imposm.parser import OSMParser
import json
import os.path
import sys

from .models import KircheOsm, Ref

def set_tags(kosm, dtags):
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
    return kosm


@task
def insert_church_node(data):
    kosm, created = KircheOsm.objects.get_or_create(osm_id=data['id'])

    kosm.lon = data['refs'][0]
    kosm.lat = data['refs'][1]

    kosm = set_tags(kosm, data.get('tags'))
    kosm.osm_type = 'N'

    # set mpoly and point in dataset
    kosm.set_geo()
    kosm.save()
    return True


@task
def insert_church_way(data):
    """ Insert church based on way(s).
    Needs references to points for creating the way(s)
    """
    # are all refs in database?
    ref_tuples = []
    for ref in data.get('refs'):
        x = Ref.objects.filter(osm_id=ref)
        if x:
            tpl.append(x.point.tuple)
        else:
            # not yet done / postpone one day
            raise insert_church_way(args=[data], countdown=3600)
            # or return False ??

    # now add dataset
    kosm, created = KircheOsm.objects.get_or_create(osm_id=data['id'])

    kosm.lon = data['refs'][0]
    kosm.lat = data['refs'][1]

    kosm = set_tags(kosm, data.get('tags'))
    kosm.osm_type = 'W'

    try:
        kosm.mpoly = MultiPolygon(Polygon(tuple(tpl)))
        kosm.point = kosm.mpoly.centroid
    except:
        try:
            # add first point at the end to close the ring.
            tpl.append(tpl[0])
            kosm.mpoly = MultiPolygon(Polygon(tuple(tpl)))
            kosm.point = kosm.mpoly.centroid
        except:
            # FIXME: should send us a message
            pass

    kosm.save()
    return True


@task
def insert_refs_needed(refs):
    """ Insert alls refs needed to create the ways for polygon-based churches.
    """
    for ref_id in refs:
        ref, created = Ref.objects.get_or_create(osm_id=ref_id)
        if not created:
            ref.need_update = True
        ref.save()
    return True


################################################################################

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


class GetRefs(object):
    """ Get all nodes for ways from first run.
    """

    def __init__(self):
        self.ref_id_list = Ref.objects.filter(need_update=True)

    def coords(self, coords):
        """ save all coords to corresponding ref dataset
        """
        for osmid, lon, lat in coords:
            if osmid in self.ref_id_list:
                ref_obj = Ref.objects.get(osm_id=osmid)
                ref_obj.set_point(lon, lat)
                ref_obj.need_update=False
                ref_obj.save()
                self.ref_id_list.remove(osmid)

################################################################################

@task
def add_churches(filename):
    # get churches
    churches = GetChurches()
    p = OSMParser(concurrency=4,
                  nodes_callback=churches.nodes,
                  ways_callback=churches.ways)
    p.parse(filename)
    
    update_refs.apply_async(args=[filename])
    return True


@task
def update_refs(filename):
    # get refs
    refs = GetRefs(opts)
    p = OSMParser(concurrency=4,
                  coords_callback=refs.coords)
    p.parse(filename)
    return True


# run it:
#import krprj.osm.tasks as t
#t.add_churches("/srv/spielwiese/stuttgart-regbez.osm")
