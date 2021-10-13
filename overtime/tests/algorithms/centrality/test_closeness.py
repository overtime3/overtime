import unittest

from overtime.components.graphs import TemporalGraph
from overtime.algorithms.centrality.closeness import *


class ClosenessTest(unittest.TestCase):
    """
		Tests for temporal closeness centrality methods.
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

    def test_temporal_closeness(self):
        """
			Tests that temporal_closeness returns correct values for several dummy networks. Tests both notions of
			optimality for which temporal_closeness is defined for and also tests on directed and undirected graphs.
		"""
        output_directed_fast = temporal_closeness(self.network1, optimality="fastest")
        output_undirected_fast = temporal_closeness(self.network2, optimality="fastest")
        output_directed_short = temporal_closeness(self.network1, optimality="shortest")
        output_undirected_short = temporal_closeness(self.network2, optimality="shortest")

        correct_directed_fast = {'g': 1.4928571428571429, 'j': 1.5, 'f': 0.0, 'a': 2.861111111111111, 'c': 1.5,
                                 'e': 2.392857142857143, 'h': 2.0, 'b': 0.0, 'i': 0.0, 'd': 1.0}
        correct_undirected_fast = {'c': 4.0, 'e': 5.226190476190476, 'd': 1.2, 'f': 2.492099567099567,
                                   'g': 2.170634920634921, 'h': 5.166666666666666, 'b': 2.658333333333333,
                                   'a': 2.6051587301587302, 'i': 2.6845238095238093, 'j': 1.5}
        correct_directed_short = {'a': 3.6666666666666665, 'i': 0.0, 'e': 3.0, 'd': 1.0, 'f': 0.0, 'j': 2.0, 'c': 2.0,
                                  'b': 0.0, 'g': 2.1666666666666665, 'h': 2.0}
        correct_undirected_short = {'b': 3.6666666666666665, 'g': 3.5833333333333335, 'c': 4.5, 'i': 3.6666666666666665,
                                    'e': 6.333333333333334, 'd': 1.5, 'a': 4.75, 'f': 4.083333333333334, 'j': 2.0,
                                    'h': 6.0}

        # Test fastest
        self.assertAlmostEqual(output_directed_fast["a"], correct_directed_fast["a"])
        self.assertAlmostEqual(output_directed_fast["e"], correct_directed_fast["e"])
        self.assertAlmostEqual(output_directed_fast["j"], correct_directed_fast["j"])

        self.assertAlmostEqual(output_undirected_fast["a"], correct_undirected_fast["a"])
        self.assertAlmostEqual(output_undirected_fast["e"], correct_undirected_fast["e"])
        self.assertAlmostEqual(output_undirected_fast["j"], correct_undirected_fast["j"])

        # Test shortest
        self.assertAlmostEqual(output_directed_short["a"], correct_directed_short["a"])
        self.assertAlmostEqual(output_directed_short["e"], correct_directed_short["e"])
        self.assertAlmostEqual(output_directed_short["j"], correct_directed_short["j"])

        self.assertAlmostEqual(output_undirected_short["a"], correct_undirected_short["a"])
        self.assertAlmostEqual(output_undirected_short["e"], correct_undirected_short["e"])
        self.assertAlmostEqual(output_undirected_short["j"], correct_undirected_short["j"])
