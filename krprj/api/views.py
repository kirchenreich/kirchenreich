# Create your views here.

import json

from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point, Polygon

from krprj.osm.models import KircheOsm


@login_required()
def api_status(request):
    x = ''
    if request.META.get('HTTP_APIKEY'):
        x = 'using APIKEY(%s)' % request.META.get('HTTP_APIKEY')
    return HttpResponse("Success: %s\n" % x)


def JSONResponse(**kwargs):
    """Return a HttpResponse which contains a json string based on kwargs
    Inspired by Armin Ronacher's Flask.jsonify"""

    res = HttpResponse()
    if '_code' in kwargs:
        res.status_code = kwargs['_code']
        del kwargs['_code']

    res.write(json.dumps(kwargs))
    return res


class PlacesResource(View):

    def get(self, request, *args, **kwargs):
        if 'in_bbox' not in request.GET:
            return JSONResponse(message="missing search area", _code=422)

        # Get cordinates for bbox from get parameter
        p1x, p1y, p2x, p2y = (
            float(n) for n in request.GET.get('in_bbox').split(',')
        )
        # Create min and max points with cordinates in EPSG:900913 for bbox
        p1 = Point(p1x, p1y, srid=900913)
        p2 = Point(p2x, p2y, srid=900913)

        # Transform EPSG:900913 (from OpenLayers) to EPSG:4326 (WGS64)
        p1.transform(4326)
        p2.transform(4326)

        # Create bbox which represents the visible map
        visible_map = Polygon.from_bbox(
            (p1.x, p1.y, p2.x, p2.y)
        )

        # Look for countries which are intersects by our visible map
        places = KircheOsm.objects.filter(mpoly__intersects=visible_map)

        # Is the visible map to big we limit the results to 100 places
        if visible_map.area > 100:
            places = places[0:100]

        # Create our json objects of places
        places_of_worship = []
        for place in places:

            # Use the GeoDjango Point type to transform the cordinations in
            # other epsg formats
            point = place.point
            try:
                point.transform(request.GET.get('epsg', 4326))
            except Exception:
                return JSONResponse(message='Error by epsg transformation',
                                    _code=422)

            _place = {
                'id': place.id,
                'name': place.name,
                'lon': point.x,
                'lat': point.y
            }
            places_of_worship.append(_place)

        return JSONResponse(
            places_of_worship=places_of_worship,
            places_of_worship_count=places.count()
        )
