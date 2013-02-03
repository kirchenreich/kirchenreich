# -*- coding: utf-8 -*-
from django import template

register = template.Library()


def decimal_to_direction(degfloat, coordinate_type):
    coordinate_type.lower()
    print coordinate_type
    if coordinate_type not in ('lat', 'lon'):
        raise Exception("Coordinate type must be lat or lon")
    if degfloat > 0 and coordinate_type == 'lat':
        direction = 'N'
    elif degfloat < 0 and coordinate_type == 'lat':
        direction = 'S'
    elif degfloat > 0 and coordinate_type == 'lon':
        direction = 'E'
    else:
        direction = 'W'
    return direction


def decimal_to_dms(degfloat):
    """Implementation of pseudocode from: http://en.wikipedia.org/wiki/Geographic_coordinate_conversion#Conversion_from_Decimal_Degree_to_DMS
    """
    degfloat = abs(float(degfloat))

    deg = int(degfloat)
    minutesfloat = 60 * (degfloat - deg)
    minutes = int(minutesfloat)
    secondsfloat = round(60 * (minutesfloat - minutes), 2)
    if secondsfloat == 60:
        minutes += 1
        secondsfloat = 0
    if minutes == 60:
        deg += 1
        minutes = 0
    return (deg, minutes, secondsfloat)


@register.simple_tag
def humanize_latlon(latitude, longitude):
    latitude = u"{0} {1}°{2}'{3}''".format(
        decimal_to_direction(latitude, 'lat'),
        *decimal_to_dms(latitude)
    )
    longitude = u"{0} {1}°{2}'{3}''".format(
        decimal_to_direction(longitude, 'lon'),
        *decimal_to_dms(longitude)
    )

    return "%s %s" % (latitude, longitude)


@register.simple_tag
def humanize_point(point):
    return humanize_latlon(point.y, point.x)
