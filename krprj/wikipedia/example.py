#!/usr/bin/python

import wikiextractor
from infobox import parse_infobox
from socket import gethostname

def infobox_test(page, cats):
#    ibox = parse_infobox(page)
#    for item in ibox:
#        print "Key:", item, "Value:", ibox[item]
#    print ibox
    coords = wikiextractor.find_coords(page)
    if coords:
        title = wikiextractor.get_title(page)
        print title, coords

hostname = gethostname()

if hostname == 'turmfalke':
    filename = '/home/web/enwiki-20120802-pages-articles.xml.bz2'
if hostname == 'ziegensittich':
    filename = '/home/klassrn/enwiki-20120802-pages-articles.xml.bz2'

if filename:
    wikiextractor.run(filename,
                      r"(place.*worship|church|chapel|mosque|temple|shrine|fane)",
                      infobox_test)
