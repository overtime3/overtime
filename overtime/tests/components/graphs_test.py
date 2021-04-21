
import unittest

from overtime.components import Graph, TemporalGraph
from overtime.inputs import CsvInput



class GraphBuildTest(unittest.TestCase):
    """
        Standalone test for the Graph build method.
    """

    def test_build(self):
        """
            Test that a graph can be built from an input csv.
        """
        graph = Graph('NetworkCSV')
        graph.build(CsvInput('./overtime/tests/data/network.csv'))
        graph.nodes
        self.assertTrue(bool(graph.nodes.set))
        self.assertTrue(bool(graph.edges.set))



class GraphTest(unittest.TestCase):
    """
        Tests for the Graph class.
    """

    def setUp(self):
        """
            Create a graph for use in all test methods.
        """
        self.graph = Graph('GraphTest')

        for node in ['a', 'b', 'c', 'd', 'e', 'f']:
            self.graph.add_node(node)

        for edge in ['ab', 'bc', 'cd', 'ef', 'fd', 'ec', 'af', 'db']:
            self.graph.add_edge(edge[0], edge[1])

    
    def test_add_node(self):
        """
            Test that a node can be added to the graph.
        """
        node = self.graph.add_node('g')
        self.assertIn(node, self.graph.nodes.set)


    def test_add_edge(self):
        """
            Test that an edge can be added to the graph.
        """
        edge = self.graph.add_edge('e', 'a')
        self.assertIn(edge, self.graph.edges.set)


    def test_remove_node(self):
        """
            Test that a node can be removed from the graph.
        """
        self.graph.remove_node('c')
        self.assertNotIn('c', self.graph.nodes.labels())


    def test_remove_edge(self):
        """
            Test that an edge can be removed from the graph.
        """
        self.graph.remove_edge('c-e')
        self.assertNotIn('c-e', self.graph.edges.uids())



class TemporalGraphBuildTest(unittest.TestCase):
    """
        Standalone test for the TemporalGraph build method.
    """

    def test_build(self):
        """
            Test that a temporal graph can be built from an input csv.
        """
        graph = TemporalGraph('NetworkCSV')
        graph.build(CsvInput('./overtime/tests/data/network.csv'))
        self.assertTrue(bool(graph.nodes.set))
        self.assertTrue(bool(graph.edges.set))



class TemporalGraphTest(unittest.TestCase):
    """
        Tests for the TemporalGraph class.
    """

    def setUp(self):
        """
            Create a graph for use in all test methods.
        """
        self.graph = TemporalGraph('TemporalGraphTest')

        for node in ['a', 'b', 'c', 'd', 'e']:
            self.graph.add_node(node)

        edges = {
            0: {'node1': 'a', 'node2': 'e', 'tstart': '2', 'tend': None},
            1: {'node1': 'd', 'node2': 'b', 'tstart': '9', 'tend': None},
            2: {'node1': 'a', 'node2': 'c', 'tstart': '10', 'tend': None},
            3: {'node1': 'b', 'node2': 'c', 'tstart': '9', 'tend': None},
            4: {'node1': 'd', 'node2': 'c', 'tstart': '7', 'tend': None},
            5: {'node1': 'b', 'node2': 'd', 'tstart': '6', 'tend': None},
            6: {'node1': 'e', 'node2': 'b', 'tstart': '4', 'tend': None},
            7: {'node1': 'a', 'node2': 'd', 'tstart': '7', 'tend': None},
            8: {'node1': 'd', 'node2': 'c', 'tstart': '8', 'tend': None},
            9: {'node1': 'b', 'node2': 'c', 'tstart': '10', 'tend': None},
            10: {'node1': 'b', 'node2': 'a', 'tstart': '5', 'tend': None},
            11: {'node1': 'd', 'node2': 'e', 'tstart': '7', 'tend': None},
            12: {'node1': 'c', 'node2': 'a', 'tstart': '12', 'tend': None},
            13: {'node1': 'a', 'node2': 'c', 'tstart': '12', 'tend': None}
        }
        for index, edge in edges.items():
            self.graph.add_edge(edge['node1'], edge['node2'], edge['tstart'], edge['tend'])


    def test_add_node(self):
        """
            Test that a node can be added to the temporal graph.
        """
        node = self.graph.add_node('f')
        self.assertIn(node, self.graph.nodes.set)


    def test_add_edge(self):
        """
            Test that an edge can be added to the temporal graph.
        """
        edge = self.graph.add_edge('f', 'a', 3)
        self.assertIn(edge, self.graph.edges.set)


    def test_remove_node(self):
        """
            Test that a node can be removed from the temporal graph.
        """
        self.graph.remove_node('c')
        self.assertNotIn('c', self.graph.nodes.labels())


    def test_remove_edge(self):
        """
            Test that an edge can be removed from the temporal graph.
        """
        self.graph.remove_edge('a-e|2-2')
        self.assertNotIn('a-e|2-2', self.graph.edges.uids())


    def test_get_snapshot(self):
        """
            Test getting a snapshot of the temporal graph.
        """
        snapshot = self.graph.get_snapshot(9)
        self.assertEqual(
            ['b-c', 'b-d'],
            sorted(snapshot.edges.labels())
        )


    def test_get_underlying_graph(self):
        """
            Test getting the underlying graph of the temporal graph.
        """
        underlying = self.graph.get_underlying_graph()
        self.assertEqual(
            ['a-b', 'a-c', 'a-d', 'a-e', 'b-c', 'b-d', 'b-e', 'c-d', 'd-e'],
            sorted(underlying.edges.labels())
        )


    def test_get_temporal_subgraph(self):
        """
            Test getting a temporal subgraph of the temporal graph.
        """
        subgraph = self.graph.get_temporal_subgraph([(0, 3), (7, 10)], ['d', 'b', 'c'])
        self.assertEqual(
            ['c-d|7-7', 'c-d|8-8', 'b-d|9-9', 'b-c|9-9', 'b-c|10-10'],
            subgraph.edges.uids()
        )
