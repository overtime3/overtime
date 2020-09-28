
import matplotlib.pyplot as plt

from inputs.classes import CsvInput
from components.graphs import TemporalGraph
from plots.circle import Circle

graph = TemporalGraph('TestNetwork', data=CsvInput('./network.csv'))
graph.print()

graph.edges.add('b', 'e', graph.nodes, 4)


figure, axes = plt.subplots(nrows=3, ncols=3)
times = range(0, 10)
i = 0
for row in axes:
    for col in row:
        Circle(graph.get_snapshot(times[i]), col, time=times[i])
        i += 1
        if i > 9:
            break

plt.tight_layout(pad=0.1)
figure.set_size_inches(14, 10)
figure.savefig('examples/multiplot.png', format='png')
figure.show()

input("Press enter key to exit...")
