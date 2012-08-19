#!/usr/bin/python

import wikiextractor
from infobox import parse_infobox
from socket import gethostname
import models
import json
import sys

def inserter(page, cats, title, lon, lat, sha1):
    if lon and lat:
        try:
            new_kwiki, created = models.KircheWikipedia.objects.get_or_create(title=title)
            if created:
                ibox = parse_infobox(page)
                new_kwiki.infobox=json.dumps(ibox)
                
            new_kwiki.sha1 = sha1
            new_kwiki.contents=''.join(page)
            if not isinstance(lon, bool):
                new_kwiki.lon=lon
            if not isinstance(lat, bool):
                new_kwiki.lat=lat
            new_kwiki.save()

            sys.stdout.write('.')
            sys.stdout.flush()
        except:
            sys.stderr.write('\n!!!!ERROR inserting %s\n'%title)
            sys.stderr.flush()

def insert():
    hostname = gethostname()

    if hostname == 'turmfalke':
        filename = '/home/web/enwiki-20120802-pages-articles.xml.bz2'
    if hostname == 'ziegensittich':
        filename = '/home/klassrn/enwiki-20120802-pages-articles.xml.bz2'
        
    if filename:
        wikiextractor.run(filename,
                          r"\[\[category:.*(place.*worship|church|chapel|mosque|temple|shrine|fane|cathedral|abbey)",
                          inserter)
