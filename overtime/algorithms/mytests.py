from overtime.components.graphs import *
from overtime.algorithms.centrality.betweenness import *

test_graph = TemporalGraph("Test Graph")

test_graph.add_node("A")
test_graph.add_node("B")
test_graph.add_node("C")
test_graph.add_node("D")
test_graph.add_node("E")
test_graph.add_node("F")
test_graph.add_node("G")
test_graph.add_node("H")


test_graph.add_edge("C", "A", 1, 1)
test_graph.add_edge("E", "A", 2, 2)
test_graph.add_edge("G", "A", 3, 3)
test_graph.add_edge("C", "B", 4, 4)
test_graph.add_edge("A", "C", 5, 5)
test_graph.add_edge("B", "A", 6, 6)
test_graph.add_edge("C", "G", 7, 7)
test_graph.add_edge("H", "E", 8, 8)
test_graph.add_edge("D", "E", 9, 9)
test_graph.add_edge("F", "E", 10, 10)
test_graph.add_edge("B", "E", 11, 11)
test_graph.add_edge("F", "E", 12, 12)

print(temporal_betweenness_centrality(test_graph))
