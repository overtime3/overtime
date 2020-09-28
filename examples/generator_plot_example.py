
from generators.nx_random import RandomGNP
from components.graphs import TemporalGraph
from plots.plotter import Plotter
from plots.circle import Circle
from plots.slice import Slice

data0 = RandomGNP(n=20, p=0.1)
graph0 = TemporalGraph('TestNetwork', data=data0)

graph0.details()


myplotter = Plotter()
myplotter.single(Slice, graph0)

myplotter.multi(
    Circle,
    [
        graph0.get_snapshot(0),
        graph0.get_snapshot(1),
        graph0.get_snapshot(2),
        graph0.get_snapshot(3),
        graph0.get_snapshot(4),
        graph0.get_snapshot(5),
        graph0.get_snapshot(6),
        graph0.get_snapshot(7),
        graph0.get_snapshot(8),
        graph0.get_snapshot(9),
        graph0.get_snapshot(10),
    ],
    ordered=True
)

input("Press enter key to exit...")
