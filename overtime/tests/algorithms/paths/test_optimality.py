import unittest

from overtime.components.digraphs import TemporalDiGraph
from overtime.algorithms.paths.optimality import *


class OptimalityTest(unittest.TestCase):
    """
		Tests functions which find optimal path metrics in temporal directed graphs.
	"""

    def setUp(self):
        """
            Create a graph for use in all test methods.
        """
        self.network1 = TemporalDiGraph("test_network")

        for node in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]:
            self.network1.add_node(node)

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

    def test_calculate_fastest_path_durations(self):
        """
			Tests that calculate_fastest_path_durations returns known correct values for several dummy networks.
		"""

        output_a = calculate_fastest_path_durations(self.network1, "a")
        output_e = calculate_fastest_path_durations(self.network1, "e")
        output_j = calculate_fastest_path_durations(self.network1, "j")

        correct_a = {'d': float('inf'), 'h': 6, 'c': 1, 'g': float('inf'), 'j': float('inf'), 'a': 0, 'e': 1, 'i': 9, 'f': 2, 'b': 12}
        correct_e = {'d': float('inf'), 'h': 1, 'c': float('inf'), 'g': float('inf'), 'j': float('inf'), 'a': float('inf'), 'e': 0, 'i': 4, 'f': 1, 'b': 7}
        correct_j = {'d': float('inf'), 'h': 1, 'c': float('inf'), 'g': float('inf'), 'j': 0, 'a': float('inf'), 'e': float('inf'), 'i': 3, 'f': float('inf'), 'b': 6}

        self.assertEqual(output_a, correct_a)
        self.assertEqual(output_e, correct_e)
        self.assertEqual(output_j, correct_j)

    def test_calculate_shortest_path_lengths(self):
        """
			Tests that calculate_shortest_path_lengths returns known correct values for several dummy networks.

			- TemporalGraph
				- 1 - 2 networks
			- TemporalDiGraph
				- 1 - 2 networks
			-
		"""

        output_a = calculate_shortest_path_lengths(self.network1, "a")
        output_e = calculate_shortest_path_lengths(self.network1, "e")
        output_j = calculate_shortest_path_lengths(self.network1, "j")

        correct_a = {'j': float('inf'), 'd':float('inf'), 'f': 2, 'c': 1, 'g': float('inf'), 'i': 3, 'b': 3, 'h': 2, 'e': 1, 'a': 0}
        correct_e = {'j': float('inf'), 'd': float('inf'), 'f': 1, 'c': float('inf'), 'g': float('inf'), 'i': 2, 'b': 2, 'h': 1, 'e': 0, 'a': float('inf')}
        correct_j = {'j': 0, 'd': float('inf'), 'f': float('inf'), 'c': float('inf'), 'g': float('inf'), 'i': 2, 'b': 2, 'h': 1, 'e': float('inf'), 'a': float('inf')}

        self.assertEqual(output_a, correct_a)
        self.assertEqual(output_e, correct_e)
        self.assertEqual(output_j, correct_j)
