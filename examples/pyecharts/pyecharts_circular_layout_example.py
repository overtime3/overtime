import overtime as ot

# load data (simple network)
network1 = ot.TemporalDiGraph('test_network', data=ot.CsvInput('../../overtime/data/network.csv'))


# load data (London subway stations - Victoria)
tfl_data = ot.CsvInput('../../overtime/data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv')
network2 = ot.TemporalDiGraph('TflNetwork', data=tfl_data)
network2.nodes.add_data('../../overtime/data/victoria_central_bakerloo_piccadilly-stations.csv')

# circular layout
# simple network
# duplicate edges have different curvature
ot.echarts_Circular(network1,3,path='../html/network_circular_layout1.html',title='circular layout with different curvature', subtitle='simple network')

# circular layout
# simple network
# duplicate edges have the same curvature
ot.echarts_Circular(network1,3,curve_list=[0.3],path='../html/network_circular_layout2.html', title='circular layout with the same curvature', subtitle='simple network')

# circular layout
# London subway stations - Victoria
# duplicate edges have the same curvature
# don't show edge value
ot.echarts_Circular(network2,100,curve_list=[0.3], show_edge_value=False,path='../html/network_circular_layout3.html', title='circular layout with the same curvature', subtitle='London subway stations')