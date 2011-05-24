#!/usr/bin/env python

import json
import urllib
import urllib2
from threading import Thread
from BeautifulSoup import BeautifulSoup

YAHOOAPPID = "Jyr2PK3e"
TIMEOUT = 10

class Geocode(Thread):

    def __init__(self, human_addr, service):
        Thread.__init__(self)
        self.human_addr = human_addr
        self.service = service
        self.lat = None
        self.lng = None
        self.addr = None

    def _submit_geocode_request(self, url):
        out = urllib2.urlopen(url, None, TIMEOUT)
        resp = "\n".join(out.readlines())
        return resp

    def _yahoo_geocode(self):
        """Submits the geocode request to Yahoo! Parses and sets
        lat/long"""
        url = "http://where.yahooapis.com/geocode?q=%s&appid=%s" % (self.addr, YAHOOAPPID)
        raw_xml = self._submit_geocode_request(url)
        xml = BeautifulSoup(raw_xml)
        latitude = xml.find("latitude").contents[0]
        longitude = xml.find("longitude").contents[0]
        self.lat = latitude
        self.lng = longitude
        print "%s N %s E" % (latitude, longitude)

    def _google_geocode(self):
        """Submits the geocode request to Google. Parses and sets
        lat/long"""
        url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % (self.addr)
        print url
        raw_json = self._submit_geocode_request(url)
        gmaps_res = json.loads(raw_json)
        lat_long = gmaps_res.get('results')[0].get('geometry').get('location')
        latitude = lat_long.get('lat')
        longitude = lat_long.get('lng')
        self.lat = latitude
        self.lng = longitude
        # print "%s N %s E" % (latitude, longitude)

    def run(self):
        self.addr = urllib.quote_plus(self.human_addr)
        if ("yahoo" == self.service):
            self._yahoo_geocode()
        elif ("google" == self.service):
            self._google_geocode()

def main():
    human_addrs = ["Mpeasem, Volta, Ghana"]

    geocoders = [Geocode(human_addr, "google") for human_addr in human_addrs]
    
    for geocoder in geocoders:
        geocoder.start()

    for geocoder in geocoders:
        geocoder.join()
        
    for geocoder in geocoders:
        print "%s|%s" % (geocoder.lat, geocoder.lng)

if __name__=="__main__":
    main()
