import unittest

from overtime.components.graphs import TemporalGraph
from overtime.components.digraphs import TemporalDiGraph
from overtime.algorithms.centrality.degree import *


class DegreeTest(unittest.TestCase):
    """
		Tests for temporal degree centrality methods.
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

    def test_temporal_degree(self):
        """
            Tests that temporal_degree returns correct values for several dummy networks. Tests on directed and
            undirected graphs as well as for in and out degree variations.
        """
        correct_directed_in = {'i': 0.25, 'e': 0.25, 'a': 0.0, 'j': 0.0, 'd': 0.0, 'f': 0.08333333333333333, 'g': 0.0,
                               'h': 0.25, 'b': 0.16666666666666666, 'c': 0.16666666666666666}
        correct_directed_out = {'j': 0.08333333333333333, 'g': 0.08333333333333333, 'a': 0.25, 'e': 0.16666666666666666,
                                'f': 0.0, 'h': 0.4166666666666667, 'd': 0.08333333333333333, 'c': 0.08333333333333333,
                                'i': 0.0, 'b': 0.0}
        corrected_undirected = {'c': 0.25, 'f': 0.08333333333333333, 'e': 0.4166666666666667, 'i': 0.25,
                             'j': 0.08333333333333333, 'a': 0.25, 'b': 0.16666666666666666, 'g': 0.08333333333333333,
                             'd': 0.08333333333333333, 'h': 0.6666666666666666}

        output_directed_in = temporal_degree(self.network1, in_out="in")
        output_directed_out = temporal_degree(self.network1, in_out="out")
        output_undirected = temporal_degree(self.network2)

        # Test directed in
        self.assertAlmostEqual(correct_directed_in["a"], output_directed_in["a"])
        self.assertAlmostEqual(correct_directed_in["e"], output_directed_in["e"])
        self.assertAlmostEqual(correct_directed_in["h"], output_directed_in["h"])

        # Test directed out
        self.assertAlmostEqual(correct_directed_out["a"], output_directed_out["a"])
        self.assertAlmostEqual(correct_directed_out["e"], output_directed_out["e"])
        self.assertAlmostEqual(correct_directed_out["h"], output_directed_out["h"])

        # Test undirected
        self.assertAlmostEqual(corrected_undirected["a"], output_undirected["a"])
        self.assertAlmostEqual(corrected_undirected["e"], output_undirected["e"])
        self.assertAlmostEqual(corrected_undirected["h"], output_undirected["h"])
