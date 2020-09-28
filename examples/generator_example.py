
from generators.nx_random import RandomGNP
from components.graphs import TemporalGraph
from plots.plotter import Plotter
from plots.circle import Circle
from plots.slice import Slice

data0 = RandomGNP(n=20, p=0.1)
graph0 = TemporalGraph('TestNetwork [p=0.1]', data=data0)
graph0.details()

data1 = RandomGNP(n=20, p=0.05)
graph1 = TemporalGraph('TestNetwork [p=0.05]', data=data1)
graph1.details()

myplotter = Plotter()
myplotter.multi(Circle, [graph0.get_snapshot(0), graph1.get_snapshot(0)])

myplotter.multi(
    Circle,
    [
        graph1.get_snapshot(0),
        graph1.get_snapshot(1),
        graph1.get_snapshot(2),
        graph1.get_snapshot(3),
        graph1.get_snapshot(4),
        graph1.get_snapshot(5),
        graph1.get_snapshot(6),
        graph1.get_snapshot(7),
        graph1.get_snapshot(8),
        graph1.get_snapshot(9),
        graph1.get_snapshot(10),
    ]
)

myplotter.single(Slice, graph0)
myplotter.single(Slice, graph1)

input("Press enter key to exit...")
