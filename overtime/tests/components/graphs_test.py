
import unittest

from overtime.components.graphs import Graph, TemporalGraph



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
