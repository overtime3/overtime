import unittest

from overtime.components.digraphs import TemporalDiGraph
from overtime.algorithms.paths.optimality import *

class OptimalityTest(unittest.TestCase):
	"""
		Tests for optimal path metrics methods.
	"""
	

	def setUp(self):
		
		self.network1 = TemporalDiGraph("test_network")

		self.network1.add_node("A")
		self.network1.add_node("B")
		self.network1.add_node("C")
		self.network1.add_node("D")
		self.network1.add_node("E")
		self.network1.add_node("F")
		self.network1.add_node("G")
		
		self.network1.add_edge("A", "E", 1, 2)
		self.network1.add_edge("A", "B", 1, 2)
		self.network1.add_edge("B", "C", 2, 3)
		self.network1.add_edge("A", "F", 3, 4)
		self.network1.add_edge("C", "D", 4, 5)
		self.network1.add_edge("F", "G", 4, 5)
		self.network1.add_edge("E", "D", 5, 6)
		self.network1.add_edge("G", "D", 6, 7)


	def test_calculate_fastest_path_durations(self):
		"""
			Tests that calculate_fastest_path_durations returns known correct values for several dummy networks.

			- TemporalGraph
				- 1 - 2 networks
			- TemporalDiGraph
				- 1 - 2 networks
			- 
		"""

		output = calculate_fastest_path_durations(self.network1, "A")
		correct = {'D': 4, 'B': 1, 'A': 0, 'G': 2, 'C': 2, 'F': 1, 'E': 1}
		self.assertEqual(output, correct)


	def test_calculate_shortest_path_lengths(self):
		"""
			Tests that calculate_fastest_path_durations returns known correct values for several dummy networks.

			- TemporalGraph
				- 1 - 2 networks
			- TemporalDiGraph
				- 1 - 2 networks
			- 
		"""
		output = calculate_shortest_path_lengths(self.network1, "A")
		correct = {'D': 2, 'B': 1, 'F': 1, 'A': 0, 'G': 2, 'C': 2, 'E': 1}

		self.assertEqual(output, correct)
