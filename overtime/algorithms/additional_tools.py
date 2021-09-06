"""
Miscellaneous tools related to centrality.
"""
from overtime.components.digraphs import TemporalDiGraph
from operator import itemgetter


def order_centrality(centralities):
    """
        Converts a dictionary which relates nodes to centrality values, so that items are ordered by centrality
        value.
    """
    ordered_centralities = {k: v for k, v in sorted(centralities.items(), key=itemgetter(1), reverse=True)}
    return ordered_centralities


def convert_to_directed(graph):
    """
        Converts an undirected graph so each undirected edge is modelled by two bidirectional edges.

        Parameter(s):
        -------------
        graph : TemporalGraph
            An undirected temporal graph.

        Returns:
        --------
        converted_graph : TemporalDiGraph
            A digraph which has bidirected edges which represent the undirected edges of the input graph.
    """
    # Initialize
    converted_graph = TemporalDiGraph("undirected_graph")
    # Add nodes
    for node in graph.nodes.aslist():
        converted_graph.add_node(node.label)
    # Add edges in both directions for each undirected edge
    for edge in graph.edges.aslist():
        converted_graph.edges.add(edge.node1.label, edge.node2.label, graph.nodes, edge.start, edge.end)
        converted_graph.edges.add(edge.node2.label, edge.node1.label, graph.nodes, edge.start, edge.end)

    return converted_graph
