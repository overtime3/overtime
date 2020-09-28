
from overtime.components.nodes import Node, Nodes



class Edge:
    """
        A class to represent an edge on a graph.

        Parameter(s):
        -------------
        node1 : String
            The label of the node1 connection.
        node2 : String
            The label of the node2 connection.
        nodes : Nodes
            The nodes collection of the graph.

        Object Propertie(s):
        --------------------
        label : String
            The node-based label of the edge.
        uid : String
            The unique label of the edge.
        directed : Boolean
            Indicates whether the edge is directed, or undirected.
        node1 : Node
            The first connected node.
        node2 : Node
            The second connected node.
        graph : Graph
            The graph of which the edge belongs to.

        See also:
        ---------
            TemporalEdge
            Edges
            TemporalEdges
    """

    def __init__(self, node1, node2, nodes):
        self.label = str(node1) + '-' + str(node2)
        self.uid = self.label
        self.directed = False
        self.node1 = nodes.add(node1)
        self.node2 = nodes.add(node2)
        self.graph = nodes.graph
        

    def print(self):
        """
            A method of Edge.
            Returns:
            --------
                None, prints the unique label of the edge.
        """
        print(self.uid)



class TemporalEdge(Edge):
    """
        A class to represent a temporal edge on a graph.

        Parameter(s):
        -------------
        node1 : String
            The label of the node1 connection.
        node2 : String
            The label of the node2 connection.
        nodes : Nodes
            The nodes collection of the graph.
        tstart : Integer
            The start time of the temporal edge.
        tend : Integer
            The end time of the temporal edge.

        Object Propertie(s):
        --------------------
        label : String
            Inherited from Edge.
        uid : String
            Inherited from Edge.
        graph : Graph
            Inherited from Edge.
        directed : Boolean
            Inherited from Edge.
        node1 : Node
            Inherited from Edge.
        node2 : Node
            Inherited from Edge.
        graph : Graph
            Inherited from Edge.
        start : Integer
            The start time of the edge.
        end : Integer
            The end time of the edge.
        duration : Integer
            The duration of the edge.

        See also:
        ---------
            Edge
            Edges
            TemporalEdges
    """

    def __init__(self, node1, node2, nodes, tstart, tend):
        super().__init__(node1, node2, nodes)
        self.uid = str(node1) + '-' + str(node2) + '|' + str(tstart)  + '-' + str(tend)
        self.start = int(tstart)
        self.end = int(tend)
        self.duration = self.end - self.start

    
    def isactive(self, time):
        """
            A method of TemporalEdge.

            Parameter(s):
            -------------
            time : Integer
                The time to check edge activity.

            Returns:
            --------
            active : Boolean
                True/false depending on whether the edge is active at time 'time'.
        """
        return True if time >= self.start and time <= self.end else False



class Edges:
    """
        A class to represent a collection of edges on a graph.

        Parameter(s):
        -------------
        graph : Graph
            A valid Graph class/subclass.


        Object Propertie(s):
        --------------------
        set : Set
            The set of edges.
        graph : Graph
            The graph of which the edges collection belongs to.


        See also:
        ---------
            Edge
            TemporalEdge
            TemporalEdges
    """

    def __init__(self, graph):
        self.set = set() # unorderd, unindexed collection of edge objects
        self.graph = graph

    
    def aslist(self):
        """
            A method of Edges.

            Returns:
            --------
            edges : List
                The collection of edges in a list.
        """
        return list(self.set)


    def add(self, node1, node2, nodes):
        """
            A method of Edges.

            Parameter(s):
            -------------
            node1 : String
                The label of the node1 connection.
            node2 : String
                The label of the node2 connection.
            node : Nodes
                A valid Nodes class/subclass.

            Returns:
            --------
            edge : Edge
                The corresponding edge object.
        """
        node_labels = sorted([str(node1),str(node2)])
        label = '-'.join(node_labels) # alphabetically sorted label.
        # if the edge does not already exist.
        if not self.exists(str(label)):
            # add the edge to the collection.
            self.set.add(Edge(node_labels[0], node_labels[1], nodes))
        return self.get_edge_by_uid(label)


    def remove(self, label):
        """
            A method of Nodes.

            Parameter(s):
            -------------
            label : String
                The label of the node to be removed.
            graph : Graph
                A valid Graph class/subclass.

            Returns:
            --------
            None, removes the node if it exists in the graph.
        """
        # check if a node with this label already exists in the graph.
        if not self.exists(str(label)):
            print('Error: {} not found in graph {}.'.format(label, self.graph.label))
        else:
            self.set.remove(self.get_edge_by_uid(label))
            print('{} removed from graph {}.'.format(label, self.graph.label))


    def subset(self, alist):
        """
            A method of Edges.

            Parameter(s):
            -------------
            alist : List
                A list of edge objects.

            Returns:
            --------
            subset : Edges
                The corresponding Edges collection.
        """
        subset = Edges(self.graph) # the subset is linked to the original graph.
        for edge in alist:
            subset.set.add(edge)
        return subset

    
    def get_edge_by_uid(self, uid):
        """
            A method of Edges.

            Parameter(s):
            -------------
            uid : String
                The unique label of an edge.

            Returns:
            --------
            edge : Edge
                The corresponding edge object.
        """
        return next((edge for edge in self.set if edge.uid == uid), None)


    def get_edge_by_label(self, label):
        """
            A method of Edges.

            Parameter(s):
            -------------
            label : String
                The label of an edge.

            Returns:
            --------
            subset : Edges
                The corresponding collection of edges with label 'label'.
        """
        return self.subset(edge for edge in self.set if edge.label == label)


    def get_edge_by_node(self, label):
        """
            A method of Edges.

            Parameter(s):
            -------------
            label : String
                The label of a node.

            Returns:
            --------
            subset : Edges
                The corresponding collection of edges connected to node 'label'.
        """
        return self.subset(edge for edge in self.set if edge.node1.label == label or edge.node2.label == label)


    def get_edge_by_node1(self, label):
        """
            A method of Edges.

            Parameter(s):
            -------------
            label : String
                The label of a node.

            Returns:
            --------
            subset : Edges
                The corresponding collection of edges connected to node1 'label'.
        """
        return self.subset([edge for edge in self.set if edge.node1.label == label])


    def get_edge_by_node2(self, label):
        """
            A method of Edges.

            Parameter(s):
            -------------
            label : String
                The label of a node.

            Returns:
            --------
            subset : Edges
                The corresponding collection of edges connected to node2 'label'.
        """
        return self.subset([edge for edge in self.set if edge.node2.label == label])


    def exists(self, uid):
        """
            A method of Edges.

            Parameter(s):
            -------------
            uid : String
                The unique label of an edge.

            Returns:
            --------
            exists : Boolean
                True if an edge with unique label 'uid' exists in the collection.
        """
        return True if self.get_edge_by_uid(uid) is not None else False

    
    def count(self):
        """
            A method of Edges.

            Returns:
            --------
            count : Integer
                The number of edges in the collection.
        """
        return len(self.set)


    def uids(self):
        """
            A method of Edges.

            Returns:
            --------
            uids : List
                A list of edge uids in the collection.
        """
        return [edge.uid for edge in self.set]


    def labels(self):
        """
            A method of Edges.

            Returns:
            --------
            labels : List
                A list of edge labels in the collection.
        """
        return [edge.label for edge in self.set]

    
    def ulabels(self):
        """
            A method of Edges.

            Returns:
            --------
            labels : List
                A list of unique edge labels in the collection.
        """
        return list(set([edge.label for edge in self.set]))

    
    def print(self):
        """
            A method of Edges.

            Returns:
            --------
                None, calls print for each edge in the collection.
        """
        print('Edges:')
        for edge in self.set:
            edge.print()



class TemporalEdges(Edges):
    """
        A class to represent a collection of temporal edges on a graph.

        Parameter(s):
        -------------
        graph : Graph
            A valid Graph class/subclass.


        Object Propertie(s):
        --------------------
        graph : Graph
            Inherited from Edges.
        set : Set
            The list of edges, ordered by edge start time.


        See also:
        ---------
            Edge
            TemporalEdge
            Edges
    """

    def __init__(self, graph):
        super().__init__(graph)
        self.set = [] # ordered (by time), indexed collection of edge objects


    def add(self, node1, node2, nodes, tstart, tend=None):
        """
            A method of TemporalEdges.

            Parameter(s):
            -------------
            node1 : String
                The label of the node1 connection.
            node2 : String
                The label of the node2 connection.
            nodes : Nodes
                A valid Nodes class/subclass.
            tstart : Integer
                The start time of the temporal edge.
            tend : Integer
                The end time of the temporal edge.

            Returns:
            --------
            edge : TemporalEdge
                The corresponding temporal edge object.
        """
        # if no end time is specified.
        if tend is None:
            tend = int(tstart) + 0 # default duration of 0.
        node_labels = sorted([str(node1),str(node2)])
        uid = '-'.join(node_labels) + '|' + str(tstart) + '-' + str(tend) # uid is alphabetically sorted.
        # if an edge with this uid does not exist in the collection.
        if not self.exists(uid):
            # create the temporal edge.
            edge = TemporalEdge(node_labels[0], node_labels[1], nodes, tstart, tend)
            # add the new edge to the collection.
            self.set.append(edge)
            # sort the collection.
            self.set = self.sort(self.set)
        return self.get_edge_by_uid(uid)


    def subset(self, alist):
        """
            A method of TemporalEdges.

            Parameter(s):
            -------------
            alist : List
                A list of temporal edge objects.

            Returns:
            --------
            subset : TemporalEdges
                The corresponding TemporalEdges collection.
        """
        subset = TemporalEdges(self.graph)
        for edge in alist:
            subset.set.append(edge)
        # sort the subset.
        subset.set = subset.sort(subset.set)
        return subset


    def sort(self, alist, key='start'):
        """
            A method of TemporalEdges.

            Parameter(s):
            -------------
            alist : List
                A list of temporal edge objects.
            key : String
                Sort by increaing 'start' (default) or 'end' times.

            Returns:
            --------
            sorted : List
                A sorted list of temporal edges, sorted by increasing start of end times.
        """
        if key is 'end':
            return sorted(alist, key=lambda x:x.end, reverse=False)
        elif key is 'start':
            # look at operator.attrgetter for getting start time from edge (optimized)
            return sorted(alist, key=lambda x:x.start, reverse=False)


    def get_edge_by_start(self, time):
        """
            A method of TemporalEdges.

            Parameter(s):
            -------------
            time : Integer
                Check edges for this time.

            Returns:
            --------
            subset : TemporalEdges
                The corresponding collection of edges with start time 'time'.
        """
        return self.subset([edge for edge in self.set if edge.start == time])

    
    def get_edge_by_end(self, time):
        """
            A method of TemporalEdges.

            Parameter(s):
            -------------
            time : Integer
                Check edges for this time.

            Returns:
            --------
            subset : TemporalEdges
                The corresponding collection of edges with end time 'time'.
        """
        return self.subset([edge for edge in self.set if edge.end == time])


    def get_edge_by_interval(self, interval):
        """
            A method of TemporalEdges.

            Parameter(s):
            -------------
            interval : List/Tuple
                A start-end time pair, for example (3,5).

            Returns:
            --------
            subset : TemporalEdges
                The corresponding collection of edges with durations within the interval specified.
        """
        return self.subset([edge for edge in self.set if edge.start >= interval[0] and edge.end <= interval[1]])


    def get_active_edges(self, time):
        """
            A method of TemporalEdges.

            Parameter(s):
            -------------
            time : Integer
                Check edges for this time.

            Returns:
            --------
            subset : TemporalEdges
                The corresponding collection of edges which are active at time 'time'.
        """
        return self.subset(edge for edge in self.set if edge.isactive(time))


    def ulabels(self):
        """
            A method of TemporalEdges.

            Returns:
            --------
            labels : List
                A sorted list of unique edge labels in the collection.
        """
        return sorted(set([label for label in self.labels()]), key=lambda x:self.labels().index(x))
        

    def start_times(self):
        """
            A method of TemporalEdges.

            Returns:
            --------
            times : List
                A list of edge start times in the collection.
        """
        return [edge.start for edge in self.set]

    
    def end_times(self):
        """
            A method of TemporalEdges.

            Returns:
            --------
            times : List
                A list of edge end times in the collection.
        """
        return [edge.end for edge in self.set]


    def start(self):
        """
            A method of TemporalEdges.

            Returns:
            --------
            start : Integer
                The smallest start time of the collection.
        """
        return self.set[0].start
    

    def end(self):
        """
            A method of TemporalEdges.

            Returns:
            --------
            end : Integer
                The largest end time of the collection.
        """
        ends = self.sort(self.set, 'end')
        return ends[-1].end + 1


    def timespan(self):
        """
            A method of TemporalEdges.

            Returns:
            --------
            timespan : Range
                The timespan on the collection.
        """
        return range(self.start(), self.end())
