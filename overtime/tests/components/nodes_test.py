
import unittest

from overtime.components import Graph, Node, Nodes



class NodeTest(unittest.TestCase):
    """
        Tests for the Node class.
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
        
        self.node = self.graph.nodes.get('b')


    def test_node1of(self):
        """
            Test that edges which have node1 'b' can be retrieved.
        """
        edges = self.node.node1of()
        self.assertEqual(
            ['b-c', 'b-d'],
            sorted(edges.labels())
        )


    def test_node2of(self):
        """
            Test that edges which have node2 'b' can be retrieved.
        """
        edges = self.node.node2of()
        self.assertEqual(
            ['a-b'],
            sorted(edges.labels())
        )


    def test_nodeof(self):
        """
            Test that edges which have node 'b' can be retrieved.
        """
        edges = self.node.nodeof()
        self.assertEqual(
            ['a-b', 'b-c', 'b-d'],
            sorted(edges.labels())
        )


    def test_neighbours(self):
        """
            Test that neighbouring nodes of node 'b' can be retrieved.
        """
        nodes = self.node.neighbours()
        self.assertEqual(
            ['a', 'c', 'd'],
            sorted(nodes.labels())
        )



class NodesTest(unittest.TestCase):
    """
        Tests for the Nodes class.
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
        
        self.nodes = self.graph.nodes


    def test_aslist(self):
        """
            Test that nodes can be returned as a list.
        """
        nodes_list = self.nodes.aslist()
        self.assertEqual(
            6,
            len(nodes_list)
        )


    def test_as_ordered_list(self):
        """
            Test that nodes can be returned as a list.
        """
        nodes_list = self.nodes.as_ordered_list()
        node_labels = []
        for node in nodes_list:
            node_labels.append(node.label)
        self.assertEqual(
            ['a', 'b', 'c', 'd', 'e', 'f'],
            node_labels
        )


    def test_add(self):
        """
            Test that a node can be added to nodes.
        """
        node = self.nodes.add('g')
        self.assertIn(node, self.nodes.set)


    def test_remove(self):
        """
            Test that a node can be removed from nodes.
        """
        self.nodes.remove('c')
        self.assertNotIn('c', self.nodes.labels())


    def test_subset(self):
        """
            Test that a subset of nodes can be created.
        """
        node1 = self.nodes.get('a')
        node2 = self.nodes.get('b')
        subset = self.nodes.subset([node1, node2])
        self.assertEqual(
            ['a', 'b'],
            sorted(subset.labels())
        )


    def test_get(self):
        """
            Test that a node can be retrieved from nodes through it's label.
        """
        node = self.nodes.get('d')
        self.assertEqual('d', node.label)


    def test_exists(self):
        """
            Test that a node's existence in nodes can be verified through it's label.
        """
        self.assertTrue(self.nodes.exists('d'))


    def test_counts(self):
        """
            Test the number of nodes can be retrieved.
        """
        self.assertEqual(6, self.nodes.count())


    def test_labels(self):
        """
            Test that all nodes labels can be retrieved.
        """
        self.assertEqual(
            ['a', 'b', 'c', 'd', 'e', 'f'],
            sorted(self.nodes.labels())
        )
