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
        self.relre = re.compile(relwords, re.IGNORECASE)

    def generator(self):
        titlere = re.compile(r'<title>([^<]*)</title>', re.IGNORECASE)
        sha1re = re.compile(r'<sha1>([^<]*)</sha1>', re.IGNORECASE)
        latre = re.compile(r'\|\w*latitude\w*=\w*(\d+(?:\.\d*)?)',
                           re.IGNORECASE)
        lonre = re.compile(r'\|\w*longitude\w*=\w*(\d+(?:\.\d*)?)',
                           re.IGNORECASE)
        coordre = re.compile(
            r'\{\{coord\|(\d+)\|(\d+)\|(\d+)\|N\|(\d+)\|(\d+)\|(\d+)\|E',
            re.IGNORECASE)
        coord2re = re.compile(r'\{\{coord\|(\d+\.\d+)\|(\d+\.\d+)',
                              re.IGNORECASE)

        data = []
        cats = []
        title = False
        lon = False
        lat = False
        first = True
        sha1 = False
        coord_found = False
        lat_found = False
        lon_found = False
        relevant = False
        for line in self.fp:
            if line.strip() == '<page>':
                first = False
            if not first:
                data.append(line)
            if line.strip().startswith('[[Category:'):
                if not relevant:
                    ll = line.lower()  # TODO do we want lowercase?
                    found = self.relre.search(ll)
                    if found:
                        relevant = True
                cats.append(line)
            if not title:
                match = titlere.search(line)
                if match:
                    title = match.groups()[0]
            if not sha1:
                match = sha1re.search(line)
                if match:
                    sha1 = match.groups()[0]
            if 'lat_' in line:
                lat_found = True
            if 'long_' in line:
                lon_found = True
            if 'latitude' in line:
                lat_found = True
            if 'longitude' in line:
                lon_found = True
            if 'coord|' in line:
                coord_found = True
            if not (lat and lon):
                match = coordre.search(line)
                if match:
                    coord_found = True
                    lon1 = match.groups()[0:3]
                    lat1 = match.groups()[3:6]
                    lon = int(lon1[0]) + (int(lon1[1]) / 60.0) + \
                        (int(lon1[2]) / 3600.0)
                    lat = int(lat1[0]) + (int(lat1[1]) / 60.0) + \
                        (int(lat1[2]) / 3600.0)
                    lon_found = True
                    lat_found = True
                else:
                    match = coord2re.search(line)
                    if match:
                        coord_found = True
                        lon = match.groups()[0]
                        lat = match.groups()[1]
                        lon_found = True
                        lat_found = True
                    else:
                        match = latre.search(line)
                        if match:
                            lat = match.groups()[0]
                            lat_found = True
                        else:
                            match = lonre.search(line)
                            if match:
                                lon = match.groups()[0]
                                lon_found = True
            if line.strip() == '</page>':
                if not first:
                    if relevant:
                        if not (lat and lon):
                            if coord_found or lat_found or lon_found:
                                lat = True
                                lon = True
                        yield (data, cats, title, lon, lat, sha1)
                data = []
                cats = []
                title = False
                lon = False
                lat = False
                sha1 = False
                relevant = False
                coord_found = False
                lat_found = False
                lon_found = False

THREADS = 4
q = Queue(THREADS * 2)


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
    match = re.search(
        r'\{\{coord\|(\d+)\|(\d+)\|(\d+)\|N\|(\d+)\|(\d+)\|(\d+)\|E',
        text,
        re.IGNORECASE)
    if match:
        lon1 = match.groups()[0:3]
        lat1 = match.groups()[3:6]
        lon = int(lon1[0]) + (int(lon1[1]) / 60.0) + (int(lon1[2]) / 3600.0)
        lat = int(lat1[0]) + (int(lat1[1]) / 60.0) + (int(lat1[2]) / 3600.0)
        return (lon, lat)


def spawn(callback, count=THREADS):
    def worker():
        while True:
            (page, cats, title, lon, lat, sha1) = q.get()
            callback(page, cats, title, lon, lat, sha1)
            q.task_done()

    for i in xrange(count):
        t = Thread(target=worker)
        t.daemon = True
        t.start()


def run(wikifile, categories, callback, threads=THREADS):
    x = WikiExtractor(wikifile, categories)
    spawn(callback, threads)
    for stuff in x.generator():
        q.put(stuff)

    q.join()
