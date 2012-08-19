from imposm.parser import OSMParser
import json
import os.path
import sys
import argparse

"""
Extraction of all amenity="place_of_worship" from an openstreetmap dump.
Data is saved in nodes.data, ways.data and refs.data.
All correlating coordinates to the ways are saved in coords.data in the
second run.
"""

class GetChurches(object):
    """ collect all nodes and ways with amenity="place_of_worship"
    """

    def __init__(self, opts):
        """ open three files for writing the data
        """
        self.fnodes = open(os.path.join(opts.datadir, "nodes.data"), "w")
        self.fways = open(os.path.join(opts.datadir, "ways.data"), "w")
        self.frefs = open(os.path.join(opts.datadir, "refs.data"), "w")

    def __del__(self):
        self.fnodes.close()
        self.fways.close()
        self.frefs.close()

    def nodes(self, nodes):
        """ save all nodes to a file.
        every line is one node as a dict (in json)
        """
        for osmid, tags, refs in nodes:
            if 'amenity' in tags and tags.get('amenity') == 'place_of_worship':
                d = {'id': osmid, 'tags':tags, 'refs':refs}
                self.fnodes.write("%s\n" % json.dumps(d))

    def ways(self, ways):
        """ save all ways to a file.
        every line is one way as a dict (in json)
        addionally save all refs to second file.
        """
        for osmid, tags, refs in ways:
            if 'amenity' in tags and tags.get('amenity') == 'place_of_worship':
                d = {'id': osmid, 'tags':tags, 'refs':refs}
                self.fways.write("%s\n" % json.dumps(d))
                for ref in refs:
                    self.frefs.write("%d\n" % ref)

class GetRefs(object):
    """ Get all nodes for ways from first run.
    """

    def __init__(self, opts, fn=None):
        if not fn:
            fn = os.path.join(opts.datadir, "refs.data")
        self.frefs = open(self.sortrefs(fn), "r")
        self.fcoords = open(os.path.join(opts.datadir, "coords.data"), "w")
        self.osmid = self.nextref()

    def __del__(self):
        self.fcoords.close()

    def nextref(self):
        next = self.frefs.readline()
        if isinstance(next, str) and len(next.strip()):
            # all refs are integer ids
            return int(next.strip())
        return False

    def sortrefs(self, fn):
        """
        use the "sort" command of unix to sort. 
        for big files the best possible choice!
        """
        import subprocess
        fnsorted = '%s.sorted' % fn
        
        subprocess.check_call('sort -n %s > %s' % (fn, fnsorted), shell=True)
        return fnsorted

    def coords(self, coords):
        """ save all coords to corresponding refs
        every line is one node as a dict (in json)
        """
        for osmid, lon, lat in coords:
            if osmid == self.osmid:
                d = {'id': osmid, 'lon':lon, 'lat':lat}
                self.fcoords.write("%s\n" % json.dumps(d))
            if osmid >= self.osmid:
                self.osmid = self.nextref()

def options():
    parser = argparse.ArgumentParser(
        description='Extracting data from openstreetmap.')

    parser.add_argument('-f', '--file', dest='filename', metavar='filename',
                        required=True,
                        help='Import from <file>.')
    parser.add_argument('--nofirst', dest='first', default=True,
                        action='store_false',
                        help='run first step (extraction of nodes/ways)')
    parser.add_argument('--nosecond', dest='second', default=True,
                        action='store_false',
                        help='run second step (extract all reference ' +\
                        'coords in ways)')
    parser.add_argument('--datadir', dest='datadir', default='data',
                        help='folder for saving extracted data.')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False,
                        action='store_true',
                        help='verbosity')
    args = parser.parse_args()
    return args

if __name__=='__main__':

    opts = options()
    if opts.first:
        if opts.verbose:
            print("first run")
        first = GetChurches(opts)
        p = OSMParser(concurrency=4,
                      nodes_callback=first.nodes,
                      ways_callback=first.ways)
        p.parse(opts.filename)
    if opts.second:
        if opts.verbose:
            print("second run")
        second = GetRefs(opts)
        p = OSMParser(concurrency=4,
                      coords_callback=second.coords)
        p.parse(opts.filename)
