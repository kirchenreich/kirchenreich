#!/usr/bin/python

import wikiextractor
from infobox import parse_infobox
from socket import gethostname
import models
import json
import sys

def inserter(page, cats):
    ibox = parse_infobox(page)
    coords = wikiextractor.find_coords(page, ibox)
    if coords:
        title = wikiextractor.get_title(page)

        try:
            new_kwiki, created = models.KircheWikipedia.objects.get_or_create(title=title,
                                                                          infobox=json.dumps(ibox),
                                                                          contents=''.join(page),
                                                                          lon=coords[0],
                                                                          lat=coords[1])
            if created:
                #print "created", title
        except:
            sys.stderr.write('!!!!ERROR inserting %s'%title)
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
