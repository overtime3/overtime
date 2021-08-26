import overtime as ot
from matplotlib import pyplot as plt
from overtime.algorithms.paths.optimality import *

test_graph = ot.TemporalDiGraph("test_graph")

test_graph.add_node("A")
test_graph.add_node("B")
test_graph.add_node("C")
test_graph.add_node("D")
test_graph.add_node("E")
test_graph.add_node("F")
test_graph.add_node("G")

test_graph.add_edge("A", "E", 1, 2)
test_graph.add_edge("A", "B", 1, 2)
test_graph.add_edge("B", "C", 2, 3)
test_graph.add_edge("A", "F", 3, 4)
test_graph.add_edge("C", "D", 4, 5)
test_graph.add_edge("F", "G", 4, 5)
test_graph.add_edge("E", "D", 5, 6)
test_graph.add_edge("G", "D", 6, 7)

print(test_graph.edges.aslist()[0].duration)
print(test_graph.edges.end())

fastest_dur = calculate_fastest_path_durations(test_graph, "A")

print(fastest_dur)
