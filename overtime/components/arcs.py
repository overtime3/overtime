
from overtime.components.nodes import Node
from overtime.components.edges import Edge, TemporalEdge, Edges, TemporalEdges



class Arc(Edge):
    """
        A class which represents a directed edge (arc) on a graph.
    """

    def __init__(self, source, sink, nodes):
        super().__init__(source, sink, nodes)
        self.directed = True
        self.source = self.node1
        self.sink = self.node2
        


class TemporalArc(TemporalEdge):
    """
        A class which represents a time-respecting directed edge (arc) on a temporal graph.
    """

    def __init__(self, source, sink, nodes, tstart, tend):
        super().__init__(source, sink, nodes, tstart, tend)
        self.directed = True
        self.source = self.node1
        self.sink = self.node2



class Arcs(Edges):
    """
        A class which represents a collection of arcs.
    """

    def __init__(self, graph):
        super().__init__(graph)


    def add(self, source, sink, nodes):
        label = str(source) + '-' + str(sink) # directed label
        if not self.exists(label):
            self.set.add(Arc(source, sink, nodes))
        return self.get_edge_by_uid(label)


    def subset(self, alist):
        subset = Arcs(self.graph)
        for edge in alist:
            subset.set.add(edge)
        return subset


    def get_edge_by_source(self, label):
        return self.subset([edge for edge in self.set if edge.source.label == label])


    def get_edge_by_sink(self, label):
        return self.subset([edge for edge in self.set if edge.sink.label == label])



class TemporalArcs(TemporalEdges):
    """
        A class which represents a collection of temporal arcs.
    """

    def __init__(self, graph):
        super().__init__(graph)


    def add(self, source, sink, nodes, tstart, tend=None):
        if tend is None:
            tend = int(tstart) + 0 # default duration of 1
        uid = str(source) + '-' + str(sink) + '|' + str(tstart) + '-' + str(tend) # directed uid
        if not self.exists(uid):
            edge = TemporalArc(source, sink, nodes, tstart, tend)
            self.set.append(edge)
            self.set = self.sort(self.set)
        return self.get_edge_by_uid(uid)


    def subset(self, alist):
        subset = TemporalArcs(self.graph)
        for edge in alist:
            subset.set.append(edge)
        subset.set = subset.sort(subset.set)
        return subset


    def get_edge_by_source(self, label):
        return self.subset([edge for edge in self.set if edge.source.label == label])


    def get_edge_by_sink(self, label):
        return self.subset([edge for edge in self.set if edge.sink.label == label])
