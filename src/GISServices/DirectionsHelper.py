#!/usr/bin/env python
"""
Get Directions and Distance from Google Maps

No command line input yet; however, the code is designed to allow you
to input a source and destination address. The output will be the HTTP
request submitted to Google Maps, the directions that Google Maps
offered for the first set of directions, and a summary of the route
(some symbolic street name, I suppose) followed by total distance and
expected time.

Example output:

http://maps.google.com/maps?saddr=Accra%2C+Ghana&daddr=Madina%2C+Ghana
(u'Head northwest on Egypt Rd toward Fourth Ave', u'170 m')
(u'Turn right onto Gamel Abdul Nasser Ave', u'250 m')
(u'Turn left onto Castle Road', u'150 m')
(u'At the traffic circle, take the 1st exit onto Independence Ave', u'1.4 km')
(u'Continue straight onto Liberation Rd', u'600 m')
(u'Keep right at the fork', u'450 m')
(u'Continue straight to stay on Liberation Rd', u'2.4 km')
(u'Slight right to stay on Liberation Rd', u'650 m')
(u'Slight right to stay on Liberation Rd', u'2.0 km')
(u'Continue onto Legon East Rd', u'4.2 km')
(u'Turn right toward Boundary Rd', u'3.0 km')
(u'Turn left onto Boundary Rd', u'800 m')
(u'Turn right', u'140 m')
Liberation Rd and Legon East Rd (16.3 km | 27 mins)

Additional Dev Notes:

 * make sure BeautifulSoup is at least version 3.2.0 (earlier versions
   couldn't parse the Google Maps html properly)

 * http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.2.0.tar.gz
"""

import re
import urllib
import urllib2
from threading import Thread
from BeautifulSoup import BeautifulSoup

TIMEOUT = 10 # seconds

class GoogleMaps(Thread):
    def __init__(self, saddr, daddr):
        Thread.__init__(self)
        self.saddr = saddr
        self.daddr = daddr
    
    def _fetch_data(self, saddr, daddr):
        quoted_saddr = urllib.quote_plus(saddr)
        quoted_daddr = urllib.quote_plus(daddr)
        url = "http://maps.google.com/maps?saddr=%s&daddr=%s" % (quoted_saddr, quoted_daddr)
        out = urllib2.urlopen(url, None, TIMEOUT)
        return (url, out.readlines())

    def _parse_highlevel(self, soup):
        out = soup.findAll("div", { "class" : "dir-altroute-inner" })
        for elem in out:
            time, path, distance = [e.contents[0] for e in elem.findAll("div")[1:-1]]
            break # don't look at alternate routes
        return time, path, distance

    def _parse_steps(self, soup):
        count = -1
        directions = list()
        while True:
            count += 1
            out = soup.find("tbody", { "id" : "step_0_%d" % (count) })
            # interesting breaks: ("span", {"class":"dirsegtext"}) ("div", {"id":"sxdist"})
            if not out:
                break
            else:
                # print out
                direction_ml_spaces = " ".join([str(x) for x in\
                                                    out.find("span", {"class":"dirsegtext"}).contents])
                direction_ml = direction_ml_spaces.replace("  ", " ")
                direction = ''.join(BeautifulSoup(direction_ml).findAll(text=True))
                dist_enc = ''.join(out.find("div", {"id":"sxdist"}).contents)
                dist_dec = dist_enc.replace("&#160;"," ")
                dist = dist_dec.strip()
                # print dist + "\t" + direction
                directions.append((direction, dist))
        return directions

    def run(self):
        (self.url, out) = self._fetch_data(self.saddr, self.daddr)
        html = "\n".join(out) # clean the html by de-listing it.
        # Use BeautifulSoup to find the html with dist info.
        soup = BeautifulSoup(html)

        self.duration, self.path, self.distance = self._parse_highlevel(soup)
        self.directions = self._parse_steps(soup)


def main():
    gm = GoogleMaps("Accra, Ghana", "Madina, Ghana")
    gm.run()

    print gm.url
    # pretty outputs...
    for ds in gm.directions:
        print ds
    print "%s (%s | %s)" % (gm.path, gm.distance, gm.duration)

if __name__=="__main__":
    main()
