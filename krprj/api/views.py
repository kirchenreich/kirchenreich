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

        return JSONResponse(
            places_of_worship=list(places.values('id', 'name')),
            places_of_worship_count=places.count()
        )
