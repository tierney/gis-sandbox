#!/usr/bin/env python

#    'Content-Type: application/vnd.google-earth.kml+xml\n'

header = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    '<Document>\n'

    '<Style id="red">\n'
    '<IconStyle>\n'
    '<Icon>\n'
    '<href>http://maps.google.com/mapfiles/kml/paddle/red-blank.png</href>\n'
    '</Icon>\n'
    '</IconStyle>\n'
    '</Style>\n'

    '<Style id="blue">\n'
    '<IconStyle>\n'
    '<Icon>\n'
    '<href>http://maps.google.com/mapfiles/kml/paddle/blu-blank.png</href>\n'
    '</Icon>\n'
    '</IconStyle>\n'
    '</Style>\n'
    )
footer = (
    '</Document>\n'
    '</kml>'
    )

def point(name, lat, lng, color):
    kml = (
        '<Placemark>\n'
        '<name>%s</name>\n'
        '<description>%s.</description>\n'
        '<styleUrl>#%s</styleUrl>\n'
        '<Point>\n'
        '<coordinates>%s,%s</coordinates>\n'
        '</Point>\n'
        '</Placemark>\n'
       ) % (name.replace(", Volta, Ghana",""),
            name, color, lng, lat)
    print kml

def main():
    with open("../../data/villages_to_latlng.txt") as fh:
        lines = [l.strip() for l in fh.readlines()]

    print header

    for i, line in enumerate(lines):
        name, lat, lng = line.split("|")
        if i % 2 == 0:
            color = 'blue'
        else:
            color = 'red'
        point(name, lat, lng, color)

    print footer

    # Goal is to maximize distance between similar clusters (trial or control). Goal is to
    # maximize distance between trial and control places.

if __name__=="__main__":
    main()
