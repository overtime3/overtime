import unittest

import overtime as ot
from overtime.algorithms.sliding_window_temporal_vertex_cover import *
from overtime.components import Graph, TemporalGraph
from overtime.inputs import CsvInput

class SwtvcTest(unittest.TestCase):

    def setUp(self):
        """
            Create graphs.
        """
        self.Tgraph = TemporalGraph('TemporalGraphTest')

        for node in ['a', 'b', 'c', 'd', 'e']:
            self.Tgraph.add_node(node)

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
            self.Tgraph.add_edge(edge['node1'], edge['node2'], edge['tstart'], edge['tend'])

        # creat static graph
        self.graph = Graph('StaticGraphTest')

        for node in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
            self.graph.add_node(node)

        edges = {
            0: {'node1': 'a', 'node2': 'd'},
            1: {'node1': 'b', 'node2': 'd'},
            2: {'node1': 'c', 'node2': 'd'},
            3: {'node1': 'e', 'node2': 'd'},
            4: {'node1': 'd', 'node2': 'f'},
            5: {'node1': 'f', 'node2': 'h'},
            6: {'node1': 'g', 'node2': 'f'},
            7: {'node1': 'h', 'node2': 'i'},
        }
        for index, edge in edges.items():
            self.graph.add_edge(edge['node1'], edge['node2'])

        # creat single-edge temporal graph
        self.singleEdgeGraph = TemporalGraph('singleEdgeGraphTest')

        for node in ['a', 'b']:
            self.singleEdgeGraph.add_node(node)

        edges = {
            0: {'node1': 'a', 'node2': 'b', 'tstart': '1', 'tend': None},
            1: {'node1': 'a', 'node2': 'b', 'tstart': '2', 'tend': None},
            2: {'node1': 'a', 'node2': 'b', 'tstart': '6', 'tend': None},

        }
        for index, edge in edges.items():
            self.singleEdgeGraph.add_edge(edge['node1'], edge['node2'], edge['tstart'], edge['tend'])

    def test_getSubSet(self):
        set1 = ['A', 'B', 'C']
        result = [[], ['A'], ['B'], ['A', 'B'], ['C'], ['A', 'C'], ['B', 'C'], ['A', 'B', 'C']]
        subset = getSubSet(set1)
        self.assertEqual(result, subset)

    def test_delta_A_union(self):
        subset = [[], ['A'], ['B'], ['A', 'B'], ['C'], ['A', 'C'], ['B', 'C'], ['A', 'B', 'C']]
        delta2 = [{1: [], 2: []},
                 {1: [], 2: ['A']},
                 {1: [], 2: ['B']},
                 {1: [], 2: ['A', 'B']},
                 {1: [], 2: ['C']},
                 {1: [], 2: ['A', 'C']},
                 {1: [], 2: ['B', 'C']},
                 {1: [], 2: ['A', 'B', 'C']},
                 {1: ['A'], 2: []},
                 {1: ['A'], 2: ['A']},
                 {1: ['A'], 2: ['B']},
                 {1: ['A'], 2: ['A', 'B']},
                 {1: ['A'], 2: ['C']},
                 {1: ['A'], 2: ['A', 'C']},
                 {1: ['A'], 2: ['B', 'C']},
                 {1: ['A'], 2: ['A', 'B', 'C']},
                 {1: ['B'], 2: []},
                 {1: ['B'], 2: ['A']},
                 {1: ['B'], 2: ['B']},
                 {1: ['B'], 2: ['A', 'B']},
                 {1: ['B'], 2: ['C']},
                 {1: ['B'], 2: ['A', 'C']},
                 {1: ['B'], 2: ['B', 'C']},
                 {1: ['B'], 2: ['A', 'B', 'C']},
                 {1: ['A', 'B'], 2: []},
                 {1: ['A', 'B'], 2: ['A']},
                 {1: ['A', 'B'], 2: ['B']},
                 {1: ['A', 'B'], 2: ['A', 'B']},
                 {1: ['A', 'B'], 2: ['C']},
                 {1: ['A', 'B'], 2: ['A', 'C']},
                 {1: ['A', 'B'], 2: ['B', 'C']},
                 {1: ['A', 'B'], 2: ['A', 'B', 'C']},
                 {1: ['C'], 2: []},
                 {1: ['C'], 2: ['A']},
                 {1: ['C'], 2: ['B']},
                 {1: ['C'], 2: ['A', 'B']},
                 {1: ['C'], 2: ['C']},
                 {1: ['C'], 2: ['A', 'C']},
                 {1: ['C'], 2: ['B', 'C']},
                 {1: ['C'], 2: ['A', 'B', 'C']},
                 {1: ['A', 'C'], 2: []},
                 {1: ['A', 'C'], 2: ['A']},
                 {1: ['A', 'C'], 2: ['B']},
                 {1: ['A', 'C'], 2: ['A', 'B']},
                 {1: ['A', 'C'], 2: ['C']},
                 {1: ['A', 'C'], 2: ['A', 'C']},
                 {1: ['A', 'C'], 2: ['B', 'C']},
                 {1: ['A', 'C'], 2: ['A', 'B', 'C']},
                 {1: ['B', 'C'], 2: []},
                 {1: ['B', 'C'], 2: ['A']},
                 {1: ['B', 'C'], 2: ['B']},
                 {1: ['B', 'C'], 2: ['A', 'B']},
                 {1: ['B', 'C'], 2: ['C']},
                 {1: ['B', 'C'], 2: ['A', 'C']},
                 {1: ['B', 'C'], 2: ['B', 'C']},
                 {1: ['B', 'C'], 2: ['A', 'B', 'C']},
                 {1: ['A', 'B', 'C'], 2: []},
                 {1: ['A', 'B', 'C'], 2: ['A']},
                 {1: ['A', 'B', 'C'], 2: ['B']},
                 {1: ['A', 'B', 'C'], 2: ['A', 'B']},
                 {1: ['A', 'B', 'C'], 2: ['C']},
                 {1: ['A', 'B', 'C'], 2: ['A', 'C']},
                 {1: ['A', 'B', 'C'], 2: ['B', 'C']},
                 {1: ['A', 'B', 'C'], 2: ['A', 'B', 'C']}]
        self.assertEqual(delta2, delta_A_union(subset,2))

    def test_check_is_vertex_cover(self):
        test = self.Tgraph.get_temporal_subgraph((6, 9))

        a = {1: [], 2: ['a', 'c']}
        b = {1: [], 2: ['b', 'd']}
        self.assertFalse(check_is_vertex_cover(test, a))
        self.assertTrue(check_is_vertex_cover(test, b))

    def test_get_min_cardinality(self):
        test = [{1: ['A', 'C'], 2: ['B'], 3: []},
                {1: ['A'], 2: ['B', 'C'], 3: []},
                {1: [], 2: ['a', 'b', 'c'], 3: []},
                {1: ['a', 'd'], 2: ['b'], 3: []},
                {1: [], 2: ['a', 'b'], 3: []}]
        result = (2, {1: [], 2: ['a', 'b'], 3: []})
        self.assertEqual(result, get_min_cardinality(test))

    def test_vertex_cover(self):
        test = self.graph
        self.assertTrue(3 == len(vertex_cover(test)))

    def test_get_temporalgraphs_with_single_edge(self):
        test = get_temporalgraphs_with_single_edge(self.Tgraph)
        self.assertEqual(9, len(test))

    def test_single_edge_swtvc(self):
        graph = self.singleEdgeGraph
        result = [['a', 2], ['a', 6]]
        self.assertEqual(result, single_edge_swtvc(graph, 2, 7))

    def test_d_approximation_swtvc(self):
        result = d_approximation_swtvc(self.Tgraph, 2)
        result1 = 0
        result2 = 11
        for i in result.values():
            result1 += len(i)
        self.assertEqual(result1, result2)

    def test_SW_TVC(self):

        graph = self.Tgraph
        result = SW_TVC(graph, 2)
        self.assertEqual((10,7), result[0].popitem())