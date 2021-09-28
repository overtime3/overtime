import unittest

from overtime.components.digraphs import Graph, TemporalGraph, TemporalDiGraph
from overtime.algorithms.centrality.betweenness import *


class BetweennessTest(unittest.TestCase):
    """
		Tests for temporal betweenness centrality methods.
	"""

    def setUp(self):
        """
            Create a graph for use in all test methods.
        """
        self.network1 = TemporalDiGraph("test_network")
        self.network2 = TemporalGraph("test_network")

        for node in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]:
            self.network1.add_node(node)
            self.network2.add_node(node)

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
            self.network1.add_edge(edge['node1'], edge['node2'], edge['tstart'], edge['tend'])
            self.network2.add_edge(edge['node1'], edge['node2'], edge['tstart'], edge['tend'])

    def test_temporal_betweenness(self):
        """
			Tests that  returns correct values for several dummy networks. Tests both notions of
			optimality for which temporal_closeness is defined for and also tests on directed and undirected graphs.
		"""
        output_directed_short = temporal_betweenness(self.network1, optimality="shortest")
        output_directed_foremost = temporal_betweenness(self.network1, optimality="foremost")
        output_undirected_short = temporal_betweenness(self.network2, optimality="shortest")
        output_undirected_foremost = temporal_betweenness(self.network2, optimality="foremost")

        correct_directed_short = {'g': 0.0, 'a': 0.0, 'f': 0, 'e': 7.0, 'i': 0, 'c': 0.0, 'h': 10.0, 'j': 0.0, 'd': 0.0,
                                 'b': 0}
        correct_directed_foremost = {'g': 0.0, 'h': 10.0, 'b': 0, 'f': 0, 'i': 0, 'c': 0.0, 'd': 0.0, 'j': 0.0, 'e': 7.0,
                                    'a': 0.0}
        correct_undirected_short = {'g': 0.0, 'b': -8.881784197001252e-16, 'h': 33.33333333333333, 'd': 0.0, 'i': 0.0,
                                    'e': 23.5, 'c': 9.5, 'a': 1.666666666666666, 'f': 0.0, 'j': 0.0}
        correct_undirected_foremost = {'j': 0.0, 'e': 26.0, 'a': 0.0, 'g': 0.0, 'b': 0.0, 'c': 10.0,
                                      'h': 40.00000000000001, 'f': 0.0, 'd': 0.0, 'i': -8.881784197001252e-16}

        # Test shortest
        self.assertAlmostEqual(output_directed_short["a"], correct_directed_short["a"])
        self.assertAlmostEqual(output_directed_short["e"], correct_directed_short["e"])
        self.assertAlmostEqual(output_directed_short["h"], correct_directed_short["h"])

        self.assertAlmostEqual(output_undirected_short["a"], correct_undirected_short["a"])
        self.assertAlmostEqual(output_undirected_short["e"], correct_undirected_short["e"])
        self.assertAlmostEqual(output_undirected_short["h"], correct_undirected_short["h"])

        # Test foremost
        self.assertAlmostEqual(output_directed_foremost["a"], correct_directed_foremost["a"])
        self.assertAlmostEqual(output_directed_foremost["e"], correct_directed_foremost["e"])
        self.assertAlmostEqual(output_directed_foremost["j"], correct_directed_foremost["j"])

        self.assertAlmostEqual(output_undirected_foremost["a"], correct_undirected_foremost["a"])
        self.assertAlmostEqual(output_undirected_foremost["e"], correct_undirected_foremost["e"])
        self.assertAlmostEqual(output_undirected_foremost["j"], correct_undirected_foremost["j"])
