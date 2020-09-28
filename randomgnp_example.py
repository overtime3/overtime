
import overtime as ot

network_data = ot.RandomGNP(n=5, p=0.25, start=1, end=10)
network = ot.TemporalGraph("RandomGNP [n:5, p:0.25]", data=network_data)

network.details()

network.nodes
network.nodes.aslist()[:2]
network.nodes.labels()

network.edges
network.edges.aslist()[:2]
network.edges.labels()[:6]
network.edges.uids()[:6]
network.edges.start_times()[:6]
ot.Slice(network)

network.edges.timespan()
snapshot = network.get_snapshot(3)
snapshot.nodes
snapshot.edges
snapshot.edges.labels()
ot.Circle(snapshot)

input("Press enter key to exit...")
