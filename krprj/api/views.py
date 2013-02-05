# Create your views here.

import json

from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point, Polygon
from django.db.models import Count

from krprj.osm.models import KircheOsm
from krprj.krunite.models import KircheUnite

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
        try:
            p1x, p1y, p2x, p2y = (
                float(n) for n in request.GET.get('in_bbox').split(',')
                )
        except ValueError:
            return JSONResponse(message="wrong data in parameter in_bbox",
                                _code=422)
        # Create min and max points with cordinates in EPSG:900913 for bbox
        p1 = Point(p1x, p1y, srid=request.GET.get('epsg', 4326))
        p2 = Point(p2x, p2y, srid=request.GET.get('epsg', 4326))

        # Transform EPSG:900913 (from OpenLayers) to EPSG:4326 (WGS64)
        p1.transform(srid=4326)
        p2.transform(srid=4326)

        # Create bbox which represents the visible map
        visible_map = Polygon.from_bbox(
            (p1.x, p1.y, p2.x, p2.y)
        )

        # Is the visible map to big we don't response places
        if visible_map.area > 10:
            return JSONResponse(message="search area to big", _code=422)

        # Look for countries which are intersects by our visible map limited
        # by GET parameter or max value
        limit = request.GET.get('limit', 500)
        places = KircheUnite.objects \
                            .filter(point__contained=visible_map)[0:limit]

        # religion statistic
        religions = KircheUnite.objects \
                               .filter(point__contained=visible_map)\
                               .values_list('religion') \
                               .annotate(count=Count("id"))
        religions = dict(religions)
        if None in religions:
            religions['unknown'] = religions[None]
            del religions[None]

        statistics = {
            'religion': religions
        }

        # Create our json objects of places
        places_of_worship = []
        for place in places:
            # Use the GeoDjango Point type to transform the cordinations in
            # other epsg formats
            if not place.point:
                continue
            try:
                place.point.transform(srid=request.GET.get('epsg', 4326))
            except Exception:
                return JSONResponse(message='Error by epsg transformation',
                                    _code=422)

            _place = {
                'id': place.pk,
                'name': place.name,
                'lon': place.point.x,
                'lat': place.point.y,
                'religion': place.religion,
                'denomination': place.denomination,
            }
            places_of_worship.append(_place)

        return JSONResponse(
            request_id=request.GET.get('request_id'),
            places_of_worship=places_of_worship,
            places_of_worship_count=places.count(),
            statistics=statistics
        )
