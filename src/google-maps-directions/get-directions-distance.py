#!/usr/bin/env python

import urllib
import urllib2

TIMEOUT=10 # seconds

class GoogleMaps(object):
    def __init__(self):
        pass
    
    def _fetch_data(self, saddr, daddr):
        """
        wget http://maps.google.com/maps?saddr={start address}&daddr={destination address}
        http://maps.google.com/maps?saddr=Obuasi,%20Ghana&daddr=Accra,%20Ghana
        """
        quoted_saddr = urllib.quote_plus(saddr)
        quoted_daddr = urllib.quote_plus(daddr)
        url = "http://maps.google.com/maps?saddr=%s&daddr=%s" % (quoted_saddr, quoted_daddr)
        
        out = urllib2.urlopen(url, None, TIMEOUT)
        return out.readlines()
        
def main():
    g = GoogleMaps()
    out = g._fetch_data("Accra, Ghana", "Madina, Ghana")
    print out
    
if __name__=="__main__":
    main()