#!/usr/bin/env python

import json
from DirectionsHelper import GoogleMaps

# all subsets
f = lambda l: reduce(lambda z, x: z + [y + [x] for y in z], l, [[]])

def tessa(source):
    """all pairs"""
    result = []
    for p1 in range(len(source)):
        for p2 in range(p1+1,len(source)):
            result.append([source[p1],source[p2]])
    return result

def format_output(inlist):
    out = ""
    for i, elt in enumerate(inlist):
        out += str(elt)
        if i+1 == len(inlist):
            break
        else:
            out += "|"
    return out

######################################################################

class AllPairs(object):
    def __init__(self):
        self.filename = "../../data/villages_to_latlng.txt"
        self.loc_data = dict()
        self.all_pairs = list()
        
    def _read_loc_data(self):
        with open(self.filename) as fh:
            lines = [line.strip() for line in fh.readlines()]

        for line in lines:
            name, lat, lng = line.split("|")
            self.loc_data[name] = (lat,lng)

    def _generate_pairs(self):
        self.all_pairs = tessa(self.loc_data.keys())

    def _format_latlng(self, pair):
        lat, lng = self.loc_data.get(pair)
        latlng = "%s, %s" % (lat, lng)
        return latlng

    def start(self):
        self._read_loc_data()
        self._generate_pairs()

        with open("all_pairs.txt","w") as fh:
            # gms = [GoogleMaps(self._format_latlng(v1), self._format_latlng(v2)) for v1,v2 in self.all_pairs]
            
            for v1, v2 in self.all_pairs:
                gm = GoogleMaps(self._format_latlng(v1),
                                self._format_latlng(v2))
                gm.run()
                pout = format_output([v1, v2, gm.url, gm.path,
                                     gm.distance, gm.duration,
                                     json.dumps(gm.directions)])
                print pout
                fh.write(pout + "\n")
                fh.flush()
        
ap = AllPairs()
ap.start()

# print ap.loc_data
