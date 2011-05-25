#!/usr/bin/env python

import networkx as nx
import matplotlib.pyplot as plt

class Pair(object):
    def __init__(self, v1, v2, url, desc, dist, dur, directions):
        self.v1 = v1
        self.v2 = v2
        self.url = url
        self.desc = desc
        self.dist = dist
        self.dur = dur
        self.directions = directions

class ParseAllPairs(object):
    def __init__(self, filename):
        self.filename = filename
        self.pairs = list()
        
    def _parse_all_pairs(self):
        with open(self.filename) as fh:
            lines = [l.strip() for l in fh.readlines()]

        for line in lines:
            v1, v2, url, desc, dist, dur, directions = line.split("|")
            pair = Pair(v1.replace(", Volta, Ghana",""),
                        v2.replace(", Volta, Ghana",""),
                        url, desc, dist, dur, directions)
            self.pairs.append(pair)

    def start(self):
        self._parse_all_pairs()
        
def main():
    AP = ParseAllPairs("../../data/village_pairs_directions.txt")
    AP.start()

    # G = nx.Graph()
    pair_weight = [(pair.v1, pair.v2, float(pair.dist.replace(" km",""))) for pair in AP.pairs]
    for d1, d2, w in pair_weight:
        print w, d1, d2
    # G.add_weighted_edges_from(pair_weight)

    # pos = nx.spring_layout(G)
    # print pos
    # # nx.draw_networkx_edges(G,pos,edgelist=pair_weight,edge_color='white')
    # nx.draw_networkx_nodes(G,pos,nodelist=G.nodes())
    # nx.draw_networkx_labels(G,pos,nodelist=G.nodes())
    # plt.show()
    

if __name__=="__main__":
    main()
            
