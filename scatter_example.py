
import overtime as ot

network = ot.TemporalDiGraph('TflNetwork', data=ot.CsvInput('./data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv'))

# further into sampled data timespan.
sub_network2 = network.get_temporal_subgraph((900, 910))
sub_network2.nodes.add_data('./data/victoria_central_bakerloo_piccadilly-stations.csv')
for node in sub_network2.nodes.set:
    node.data['reachability'] = ot.calculate_reachability(sub_network2, node.label)


# show Oxford Circus' foremost tree.
oxcircus_tree = ot.calculate_foremost_tree(sub_network2, 'Oxford Circus')
oxcircus_tree.nodes.add_data('./data/victoria_central_bakerloo_piccadilly-stations.csv')

ot.NodeLink(oxcircus_tree, x='lon', y='lat', bubble_metric='foremost_time')

input("Press enter key to exit...")
