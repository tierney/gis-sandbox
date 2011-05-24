#!/usr/bin/env python

from VillageParser import VillageParser
from Geocoding import Geocode

def main():
    vp = VillageParser("../../data/villages.txt")
    vp.start()
    villages = vp.villages

    for i, vill in enumerate(villages):
        print i, vill

    human_addrs = villages

    geocoders = [Geocode(human_addr, "google") for human_addr in human_addrs]
    
    for geocoder in geocoders:
        geocoder.start()

    for geocoder in geocoders:
        geocoder.join()
        
    for geocoder in geocoders:
        print "%s|%s|%s" % (geocoder.human_addr, geocoder.lat, geocoder.lng)

if __name__=="__main__":
    main()
