
from generators.nx_random import RandomGNP
from inputs.classes import CsvInput
from components.graphs import TemporalGraph
from plots.plotter import Plotter
from plots.slice import Slice

data1 = RandomGNP(n=10, p=0.25, end=50)
graph1 = TemporalGraph('TestNetwork [p=0.1]', data=data1)
graph1.details()
myplotter = Plotter()
myplotter.single(Slice, graph1)

graph = TemporalGraph('TestNetwork', data=CsvInput('./network.csv'))
graph.add_node('x')
graph.add_edge('f', 'a', 3, 7)
graph.details()

myplotter = Plotter()
myplotter.single(Slice, graph)

input("Press enter key to exit...")
