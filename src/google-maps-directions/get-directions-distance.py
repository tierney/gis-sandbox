#!/usr/bin/env python
#make sure this is at least version 3.2.0
#http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.2.0.tar.gz

import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
from threading import Thread

TIMEOUT = 10 # seconds

import re

def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id))
    except:
        return id

def decode_unicode_references(data):
    return re.sub("&#(\d+)(;|(?=\s))", _callback, data)


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
        return out

    def _parse_steps(self, soup):
        count = -1
        while True:
            count += 1
            out = soup.find("tbody", { "id" : "step_0_%d" % (count) })
            # interesting breaks: ("span", {"class":"dirsegtext"}) ("div", {"id":"sxdist"})
            if not out:
                break
            else:
                # print out
                direction_ml = "".join([str(x) for x in out.find("span", {"class":"dirsegtext"}).contents])
                direction = ''.join(BeautifulSoup(direction_ml).findAll(text=True))
                distance = ''.join(out.find("div", {"id":"sxdist"}).contents)
                print direction, decode_unicode_references(distance).strip()

    def run(self):
        (url, out) = self._fetch_data(self.saddr, self.daddr)
        html = "\n".join(out) # clean the html by de-listing it.
        # Use BeautifulSoup to find the html with dist info.
        soup = BeautifulSoup(html)

        self.location_html = self._parse_highlevel(soup)
        self._parse_steps(soup)

def main():
    g = GoogleMaps("Accra, Ghana", "Madina, Ghana")
    g.run()
    # print g.location_html

    for soup in g.location_html:
        for div in soup.findAll("div")[:-1]:
            print " ", div.contents
            
        # print soup.find("div", { "class" : "altroute-rcol altroute-info" })

if __name__=="__main__":
    main()
