
import overtime as ot

####################
### Introduction ###
####################

### import central line data & create graph.
central = ot.TemporalDiGraph('CentralLine', data=ot.CsvInput('./data/central-inbound.csv'))
central.nodes # nodes object
central.edges # edges object

# nodes
central.nodes.aslist()[0:4]
central.nodes.count()
central.nodes.labels()

# node
lstreet = central.nodes.get('Liverpool Street')
lstreet.sourceof()
lstreet.sourceof().labels()
lstreet.sinkof().labels()
lstreet.sinkof().start_times()
lstreet.sinkof().end_times()
lstreet.nodeof().labels()
lstreet.neighbours()

# edges
central.edges.aslist()
central.edges.count()
central.edges.labels()
central.edges.start_times()
central.edges.get_edge_by_label('Bethnal Green-Liverpool Street')
central.edges.get_edge_by_source('Liverpool Street')
central.edges.get_edge_by_source('Liverpool Street').start_times()
central.edges.get_edge_by_source('Liverpool Street').get_edge_by_start(879).labels()
central.edges.get_edge_by_source('Liverpool Street').get_edge_by_interval((879, 884)).start_times()

# graph
central.details()
# snapshot
central.get_snapshot(879)
central.get_snapshot(879).details()
ot.Circle(central.get_snapshot(879))
# subgraph
central.get_temporal_subgraph((879, 900))
central.get_temporal_subgraph((879, 900)).details()
ot.Circle(central.get_temporal_subgraph((879, 884)))



#####################
### Visualization ###
#####################

# show central line.
ot.Circle(central)
ot.Slice(central)
ot.NodeScatter(central)

# show central line stations.
central.nodes.add_data('./data/central-stations.csv')
ot.NodeScatter(central, x='lon', y='lat')

# larger network (4 lines).
network = ot.TemporalDiGraph('TflNetwork', data=ot.CsvInput('./data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv'))
network.details()
network.nodes.add_data('./data/victoria_central_bakerloo_piccadilly-stations.csv')

# show larger network.
ot.NodeScatter(network)
ot.NodeScatter(network, x='lon', y='lat')
ot.Slice(network)



####################
### Reachability ###
###  & Foremost  ###
####################

# first 10mins of sampled data.
sub_network1 = network.get_temporal_subgraph((840, 850))
sub_network1.nodes.add_data('./data/victoria_central_bakerloo_piccadilly-stations.csv')
for node in sub_network1.nodes.set:
    ot.calculate_reachability(sub_network1, node.label)

# show the sub network.
ot.Circle(sub_network1)
ot.Slice(sub_network1)
ot.NodeScatter(sub_network1, y='reachability', bubble_metric='reachability', colors='bmet')
ot.NodeScatter(sub_network1, x='lon', y='lat', bubble_metric='reachability', colors='bmet')

# show brixton's foremost tree.
brixton_tree = ot.calculate_foremost_tree(sub_network1, 'Brixton')
brixton_tree.nodes.add_data('./data/victoria_central_bakerloo_piccadilly-stations.csv')
ot.Circle(brixton_tree)
ot.NodeLink(brixton_tree, x='lon', y='lat', bubble_metric='foremost_time')


# further into sampled data timespan.
sub_network2 = network.get_temporal_subgraph((900, 910))
sub_network2.nodes.add_data('./data/victoria_central_bakerloo_piccadilly-stations.csv')
for node in sub_network2.nodes.set:
    ot.calculate_reachability(sub_network2, node.label)

# show the sub network.
ot.Circle(sub_network2)
ot.Slice(sub_network2)
ot.NodeLink(sub_network2, x='lon', y='lat', bubble_metric='reachability', colors='bmet')

# show Oxford Circus' foremost tree.
oxcircus_tree = ot.calculate_foremost_tree(sub_network2, 'Oxford Circus')
oxcircus_tree.nodes.add_data('./data/victoria_central_bakerloo_piccadilly-stations.csv')
ot.Circle(oxcircus_tree)
ot.Slice(oxcircus_tree)
ot.NodeLink(oxcircus_tree, x='lon', y='lat', bubble_metric='foremost_time')

input("Press enter key to exit...")
