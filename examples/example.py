
from inputs.classes import CsvInput
from components.graphs import TemporalGraph
from components.digraphs import TemporalDiGraph
from plots.plotter import Plotter
from plots.circle import Circle



graph = TemporalGraph('TestNetwork1', data=CsvInput('./network.csv'))

# digraph = TemporalDiGraph('TestNetwork2', data=CsvInput('./network.csv'))

graph.details()
graph.print()

# digraph.details()
# digraph.print()


myplotter = Plotter()
myplotter.single(Circle, graph)
#myplotter.single(Circle, digraph)

# myplotter.multi(
#     Circle,
#     [graph.get_snapshot(6), graph.get_snapshot(7)]
# )


snapshots = []
for t in graph.edges.timespan():
    snapshots.append(graph.get_snapshot(t))

myplotter.multi(Circle, snapshots)

# snapshots = []
# for t in digraph.edges.timespan():
#     snapshots.append(digraph.get_snapshot(t))

# myplotter.multi(Circle, snapshots)

input("Press enter key to exit...")
