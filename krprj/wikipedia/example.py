#!/usr/bin/python

import wikiextractor
from infobox import parse_infobox
from socket import gethostname

def infobox_test(page, cats):
    ibox = parse_infobox(page)
    print ibox

hostname = gethostname()

if hostname == 'turmfalke':
    filename = '/home/web/enwiki-20120802-pages-articles.xml.bz2'
if hostname == 'ziegensittich':
    filename = '/home/klassrn/enwiki-20120802-pages-articles.xml.bz2'

if filename:
    wikiextractor.run(filename,
                      r"(place.*worship|church|chapel|mosque|temple)",
                      infobox_test)
