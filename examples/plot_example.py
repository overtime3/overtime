
import matplotlib.pyplot as plt

from inputs.classes import CsvInput
from components.digraphs import TemporalDiGraph
from algorithms.foremost import calculate_foremost_tree
from plots.circle import Circle

graph = TemporalDiGraph('TestNetwork', data=CsvInput('./network.csv'))
graph.print()

figure, axes = plt.subplots(1)
Circle(graph, axes, 'TestNetwork')

plt.tight_layout(pad=0.1)
figure.set_size_inches(14, 10)
figure.savefig('examples/graph.png', format='png')

figure, axes = plt.subplots(nrows=2, ncols=2)
foremost_a = calculate_foremost_tree(graph, 'a')
Circle(foremost_a, axes[0][0], 'root: a')

foremost_b = calculate_foremost_tree(graph, 'b')
Circle(foremost_b, axes[0][1], 'root: b')

foremost_c = calculate_foremost_tree(graph, 'c')
Circle(foremost_c, axes[1][0], 'root: c')

foremost_d = calculate_foremost_tree(graph, 'd')
Circle(foremost_d, axes[1][1], 'root: d')

plt.tight_layout(pad=0.1)
figure.set_size_inches(14, 10)
figure.savefig('examples/foremost_trees.png', format='png')

plt.show()

input("Press enter key to exit...")
