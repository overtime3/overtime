import overtime as ot
from matplotlib import pyplot as plt
from overtime.algorithms.centrality.pagerank import *

network1 = ot.TemporalDiGraph("test_network")

for node in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]:
    network1.add_node(node)

edges = {
    0: {'node1': 'a', 'node2': 'e', 'tstart': 1, 'tend': 2},
    1: {'node1': 'e', 'node2': 'f', 'tstart': 2, 'tend': 3},
    2: {'node1': 'g', 'node2': 'e', 'tstart': 3, 'tend': 4},
    3: {'node1': 'h', 'node2': 'b', 'tstart': 4, 'tend': 5},
    4: {'node1': 'h', 'node2': 'i', 'tstart': 5, 'tend': 6},
    5: {'node1': 'e', 'node2': 'h', 'tstart': 6, 'tend': 7},
    6: {'node1': 'c', 'node2': 'h', 'tstart': 7, 'tend': 8},
    7: {'node1': 'j', 'node2': 'h', 'tstart': 7, 'tend': 8},
    8: {'node1': 'd', 'node2': 'c', 'tstart': 8, 'tend': 9},
    9: {'node1': 'h', 'node2': 'i', 'tstart': 9, 'tend': 10},
    10: {'node1': 'h', 'node2': 'i', 'tstart': 10, 'tend': 11},
    11: {'node1': 'a', 'node2': 'e', 'tstart': 11, 'tend': 12},
    12: {'node1': 'h', 'node2': 'b', 'tstart': 12, 'tend': 13},
    13: {'node1': 'a', 'node2': 'c', 'tstart': 12, 'tend': 13}
}

for index, edge in edges.items():
    network1.add_edge(edge['node1'], edge['node2'], edge['tstart'], edge['tend'])

output = temporal_pagerank(network1)
print(output)
