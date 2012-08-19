# -*- coding: utf-8 -*-

import bz2
import codecs
import re
from Queue import Queue
from threading import Thread
from infobox import parse_infobox

class WikiExtractor:

    def __init__(self, fn, relwords):
        self.fp = codecs.getreader('utf-8')(bz2.BZ2File(fn), errors='replace')
        self.relre = re.compile(relwords)

    def generator(self):
        data = []
        cats = []
        first = True
        relevant = False
        for line in self.fp:
            if line.strip() == '<page>':
                first = False
            if not first:
                data.append(line)
            if line.strip().startswith('[[Category:'):
                if not relevant:
                    ll = line.lower() # TODO do we want lowercase?
                    found = self.relre.search(ll)
                    if found:
                        relevant = True
                cats.append(line)
            if line.strip() == '</page>':
                if not first:
                    if relevant:
                        yield (data, cats)
                data = []
                cats = []
                relevant = False

THREADS=4
q = Queue(THREADS*2)

def get_title(page):
    titlere = re.compile(r'<title>([^<]*)</title>', re.IGNORECASE)
    for line in page:
        match = titlere.search(line)
        if match:
            return match.groups()[0]

def find_coords(page, ibox=False):
    lat = False
    lon = False
    if not ibox:
        ibox = parse_infobox(page)
    if 'latitude' in ibox:
        lat = ibox['latitude']
    elif 'Latitude' in ibox:
        lat = ibox['Latitude']
    if lat:
        if 'longitude' in ibox:
            lon = ibox['longitude']
        elif 'Longitude' in ibox:
            lon = ibox['Longitude']
    if lat and lon:
        return (lon, lat)
    
    text = ''.join(page)
    match = re.search(r'\{\{coord\|(\d+)\|(\d+)\|(\d+)\|N\|(\d+)\|(\d+)\|(\d+)\|E', text, re.IGNORECASE)
    if match:
        lon1 = match.groups()[0:3]
        lat1 = match.groups()[3:6]
        lon = int(lon1[0]) + (int(lon1[1]) / 60.0) + (int(lon1[2]) / 3600.0)
        lat = int(lat1[0]) + (int(lat1[1]) / 60.0) + (int(lat1[2]) / 3600.0)
        return (lon, lat)


def spawn(callback, count=THREADS):
    def worker():
        while True:
            (page, cats) = q.get()
            callback(page, cats)
            q.task_done()

    for i in xrange(count):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
        
def run(wikifile, categories, callback, threads=THREADS):
    x = WikiExtractor(wikifile, categories)
    spawn(callback, threads)
    for page in x.generator():
        q.put(page)

    q.join()

