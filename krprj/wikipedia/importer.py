#!/usr/bin/python

import wikiextractor
from infobox import parse_infobox
from socket import gethostname
import models
import json
import sys

def inserter(page, cats, title, lon, lat, sha1):
    if lon and lat:
        ibox = parse_infobox(page)
        try:
            new_kwiki, created = models.KircheWikipedia.objects.get_or_create(title=title,
                                                                          infobox=json.dumps(ibox),
                                                                          contents=''.join(page),
                                                                          lon=lon,
                                                                          lat=lat)
            new_kwiki.sha1 = sha1
            new_kwiki.save()
            # if created:
            #     print "created", title
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
                          r"(place.*worship|church|chapel|mosque|temple|shrine|fane)",
                          inserter)
