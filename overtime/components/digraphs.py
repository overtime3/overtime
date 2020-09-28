
from overtime.components.graphs import Graph, TemporalGraph
from overtime.components.nodes import Nodes
from overtime.components.arcs import Arcs, TemporalArcs



class DiGraph(Graph):
    """
        A class which represents a static, directed graph consisting of nodes and arcs.

        Parameter(s):
        -------------
        label : String
            A label for the graph.
        data : Input
            A valid Input class/subclass.

        Object Propertie(s):
        --------------------
        label : String
            Inherited from Graph.
        directed : Boolean
            Inherited from Graph.
        static : Boolean
            Inherited from Graph.
        nodes : Nodes
            Inherited from Graph.
        edges : Edges
            An arcs collection representing all edges in the graph.

        See also:
        ---------
            Graph
            TemporalGraph
            TemporalDiGraph
    """

    def __init__(self, label, data=None):
        super().__init__(label)
        self.directed = True
        self.edges = Arcs(self)

        # if input data is supplied.
        if data is not None:
            # build the graph using this data.
            self.build(data)
        


class TemporalDiGraph(TemporalGraph):
    """
        A class which represents a temporal, directed graph consisting of nodes and temporal arcs.

        Parameter(s):
        -------------
        label : String
            A label for the graph.
        data : Input
            A valid Input class/subclass.

        Object Propertie(s):
        --------------------
        label : String
            Inherited from TemporalGraph.
        directed : Boolean
            Inherited from TemporalGraph.
        static : Boolean
            Inherited from TemporalGraph.
        nodes : Nodes
            Inherited from TemporalGraph.
        edges : Edges
            An temporal arcs collection representing all edges in the graph.

        See also:
        ---------
            Graph
            Digraph
            TemporalGraph
    """

    def __init__(self, label, data=None):
        super().__init__(label)
        self.directed = True
        self.edges = TemporalArcs(self)

        # if input data is supplied.
        if data is not None:
            # build the graph using this data.
            self.build(data)


    def get_snapshot(self, time):
        """
            A method of TemporalDiGraph.

            Parameter(s):
            -------------
            time : Integer
                The time to take the snapshot at.

            Returns:
            --------
            graph : DiGraph
                A static directed graph snapshot at time 'time'.
        """
        # update graph label.
        label = self.label + ' [time: ' + str(time) + ']'
        # create static snapshot.
        graph = DiGraph(label)
        # for each edge that is active at time 'time'.
        for edge in self.edges.get_active_edges(time).set:
            # add the edge to the snapshot.
            graph.add_edge(edge.node1.label, edge.node2.label)
        # for each node in the graph.
        for node in self.nodes.set:
            # add the node to the snapshot.
            graph.add_node(node.label)
        # return the snapshot.
        return graph
