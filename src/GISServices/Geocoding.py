#!/usr/bin/env python

import json
from threading import Thread
from BeautifulSoup import BeautifulSoup

APPID = "Jyr2PK3e"
TIMEOUT = 10

class Geocode(Thread):
    def __init__(self, addr):
        Thread.__init__(self)
        self.addr = addr

    def run(self):
        pass

def main():
    human_addr = "Dodi, Volta, Ghana"

    addr = urllib.quote_plus(human_addr)
    print addr
    
    url = "http://where.yahooapis.com/geocode?q=%s&appid=%s" % (addr, APPID)
    out = urllib2.urlopen(url, None, TIMEOUT)
    raw_xml = "\n".join(out.readlines())
    xml = BeautifulSoup(raw_xml)
    latitude = xml.find("latitude").contents[0]
    longitude = xml.find("longitude").contents[0]
    print "%s N %s E" % (latitude, longitude)
    
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (addr)
    out = urllib2.urlopen(url, None, TIMEOUT)
    raw_json = "\n".join(out.readlines())
    gmaps_res = json.loads(raw_json)
    lat_long = gmaps_res.get('results')[0].get('geometry').get('location')
    latitude = lat_long.get('lat')
    longitude = lat_long.get('lng')
    print "%s N %s E" % (latitude, longitude)    

if __name__=="__main__":
    main()
