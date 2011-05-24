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
        print "AHHH!"
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
                dist_dec = dist_enc.replace("&#160;"," ") # decode_unicode_references(dist_enc).strip()
                dist = dist_dec.strip()
                # print dist + "\t" + direction
                directions.append((direction, dist))
        return directions

    def run(self):
        (url, out) = self._fetch_data(self.saddr, self.daddr)
        print url
        html = "\n".join(out) # clean the html by de-listing it.
        # Use BeautifulSoup to find the html with dist info.
        soup = BeautifulSoup(html)

        time, path, distance = self._parse_highlevel(soup)
        directions = self._parse_steps(soup)

        # pretty outputs...
        for ds in directions: print ds
        print "%s (%s | %s)" % (path, distance, time)

def main():
    GoogleMaps("Accra, Ghana", "Madina, Ghana").run()
    GoogleMaps("145 SW Salix Terrace, Beaverton, OR", "1925 Eastchester Road, Bronx, NY").run()

if __name__=="__main__":
    main()
