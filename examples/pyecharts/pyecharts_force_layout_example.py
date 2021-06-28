import overtime as ot

# load data (simple network)
network1 = ot.TemporalDiGraph('test_network', data=ot.CsvInput('../../overtime/data/network.csv'))

# load data (London subway stations - Victoria)
tfl_data = ot.CsvInput('../../overtime/data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv')
network2 = ot.TemporalDiGraph('TflNetwork', data=tfl_data)
network2.nodes.add_data('../../overtime/data/victoria_central_bakerloo_piccadilly-stations.csv')

# force layout
# nodes are draggable
ot.echarts_Force(network1,3,path='../html/network_force_layout1.html',title='force layout with draggable nodes',subtitle='simple network')

# force layout
# nodes are undraggable
ot.echarts_Force(network1,3,is_draggable=False,path='../html/network_force_layout2.html',title='force layout with undraggable nodes',subtitle='simple network')

# force layout
# London subway stations - Victoria
# don't show edge value
ot.echarts_Force(network2,100,show_edge_value=False,path='../html/network_force_layout3.html', title='force layout', subtitle='London subway stations')