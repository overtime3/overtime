#import overtime.algorithms.matching as dm
import overtime as ot
import networkx as nx

network = ot.TemporalGraph('SampleNetwork', data=ot.CsvInput('./data/network.csv'))
network.details()
network.print()

T = 15
deta = 3

ls = ot.count_matching(network, T, deta)

print()
print("Max cardinality is {}".format(len(ls)))
print("Time edges in maximum ∆-temporal matching are:")
for edge in ls:
    print(edge)

temporalList = []
timeList = set()
for edge in ls:
    node1 = edge[0].split('-')[0]
    node2 = edge[0].split('-')[1]
    node_labels = sorted([str(node1),str(node2)])
    label = '-'.join(node_labels) # alphabetically sorted label.
    tstart = edge[1] 
    temporalList.append((label, tstart))
    timeList.add(tstart)
#print(temporalList)

plotter = ot.Plotter()

snapshots = []
delList = []
for t in network.edges.timespan():
    graph = network.get_snapshot(t)
    if t in timeList:
        graph.print()
        #print(temporalList)
        for item in temporalList:
            #print(item)
            if  graph.edges.exists2(item[0]) and t == item[1] and item not in delList:
                print("---")
                #temporalList.remove(item)
                delList.append(item)
                graph.remove_edge2(item[0])
                graph.add_edge(item[0].split('-')[0], item[0].split('-')[1], True)
               
   
    snapshots.append(graph)

plotter.multi(ot.Circle, snapshots)
