#!/usr/bin/env python

class VillageParser(object):
    def __init__(self, filename):
        self.filename = filename
        self.villages = list()
        
    def _decomment(self, village_lines):
        # Remove comment lines
        villages = list()
        for line in village_lines:
            # empty line
            if not line:
                continue

            hash_pos = line.find("#")
            if hash_pos == 0:
                continue
            elif hash_pos > 0:
                villages.append(line[:hash_pos])
            else:
                villages.append(line)
        return villages

    def start(self):
        with open(self.filename) as fh:
            village_lines = [l.strip() for l in fh.readlines()]

        self.villages = self._decomment(village_lines)

def main():
    vp = VillageParser("../../data/villages.txt")
    vp.start()
    villages = vp.villages

    for i, vill in enumerate(villages):
        print i, vill

if __name__=="__main__":
    main()
