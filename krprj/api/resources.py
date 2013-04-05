import json

from django.contrib.gis.geos import Point, Polygon

from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.exceptions import InvalidFilterError, BadRequest

from krprj.krunite.models import KircheUnite
from krprj.osm.models import KircheOsm
from krprj.wikipedia.models import KircheWikipedia


class OSMPlacesResource(GeoModelResource):

    class Meta:
        queryset = KircheOsm.objects.all()
        allowed_methods = ['get']
        resource_name = 'osm_places'
        max_limit = 50

    place = fields.ToOneField('krprj.api.resources.PlacesResource', 'unite',
                              null=True)

    def dehydrate_addional_fields(self, bundle):
        return json.loads(bundle.data.get('addional_fields', '{}'))


class WikipediaArticleResource(GeoModelResource):

    class Meta:
        queryset = KircheWikipedia.objects.all()
        allowed_methods = ['get']
        resource_name = 'wikipedia_articles'
        max_limit = 50

    contents = fields.CharField(attribute='contents', null=True,
                                use_in='detail')

    place = fields.ToOneField('krprj.api.resources.PlacesResource', 'unite',
                              null=True)

    def dehydrate_infobox(self, bundle):
        return json.loads(bundle.data['infobox'])


class PlacesResource(GeoModelResource):

    osm_places = fields.ToManyField(OSMPlacesResource, 'kircheosm_set',
                                    full=False, use_in='detail')
    wikipedia_articles = fields.ToManyField(WikipediaArticleResource,
                                            'kirchewikipedia_set',
                                            full=False, use_in='detail')

    class Meta:
        queryset = KircheUnite.objects.all()
        allowed_methods = ['get']
        resource_name = 'places'

        filtering = {
            "name": ('exact', 'startswith', 'contains')
        }
        max_limit = 500

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(PlacesResource, self).build_filters(filters)

        if 'in_bbox' in filters:
            try:
                p1x, p1y, p2x, p2y = (
                    float(n) for n in filters['in_bbox'].split(',')
                )
            except ValueError:
                raise InvalidFilterError("There was a error by 'in_bbox' "
                                         "filter.")

            p1 = Point(p1x, p1y)
            p2 = Point(p2x, p2y)

            p1.transform(4326)
            p2.transform(4326)

            # Create bbox which represents the visible map
            bbox = Polygon.from_bbox(
                (p1.x, p1.y, p2.x, p2.y)
            )

            if bbox.area > 10:
                raise BadRequest("The search area is to big")

            orm_filters['point__contained'] = bbox

        return orm_filters

    def alter_list_data_to_serialize(self, request, data):
        if 'request_id' in request.GET:
            data['meta']['request_id'] = request.GET['request_id']
        return data
