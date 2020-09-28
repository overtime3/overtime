
import math
import pandas as pd



class Node:
    """
        A class to represent a node on a graph.

        Parameter(s):
        -------------
        label : String
            A label for the node.
        graph : Graph
            A valid Graph class/subclass.

        Object Propertie(s):
        --------------------
        label : String
            The label of the node.
        graph : Graph
            The graph of which the node belongs to.
        data : Dictionary
            A dictionary to be used for adding ambiguous data to a node.

        See also:
        ---------
            ForemostNode
            Nodes
            ForemostNodes
    """

    def __init__(self, label, graph):
        self.label = str(label)
        self.graph = graph
        self.data = dict()


    def print(self):
        """
            A method of Node.

            Returns:
            --------
                None, prints the label of the node.
        """
        print(self.label)


    def node1of(self, time=None):
        """
            A method of Node.

            Parameter(s):
            -------------
            time : Integer
                Time to check connectivity.

            Returns:
            --------
            edges : Edges
                An edges class/subclass object.
                The collection of edges returned each have the node1 property of this node (self).
        """
        # if a time was specified.
        if time is not None:
            # get all graph edges that are active at this time.
            edges = self.graph.edges.get_active_edges(time)
        else:
            # no time was specified, get all the graph's edges.
            edges = self.graph.edges
        # return the edges that have this node as their 'node1' property.
        return edges.get_edge_by_node1(self.label)

    
    def sourceof(self, time=None):
        """
            A method of Node.

            Parameter(s):
            -------------
            time : Integer
                Time to check connectivity.

            Returns:
            --------
            edges : Edges
                An edges class/subclass object.
                The collection of edges returned each have the sourceof property of this node (self).
        """
        # return node1of (analogous property)
        return self.node1of(time)


    def node2of(self, time=None):
        """
            A method of Node.

            Parameter(s):
            -------------
            time : Integer
                Time to check connectivity.

            Returns:
            --------
            edges : Edges
                An edges class/subclass object.
                The collection of edges returned each have the node2 property of this node (self).
        """
        # if time was specified.
        if time is not None:
            # get all graph edges that are active at this time.
            edges = self.graph.edges.get_active_edges(time)
        else:
            # no time was specified, get all the graph's edges.
            edges = self.graph.edges
        # return the edges that have this node as their 'node2' property.
        return edges.get_edge_by_node2(self.label)

    
    def sinkof(self, time=None):
        """
            A method of Node.

            Parameter(s):
            -------------
            time : Integer
                Time to check connectivity.

            Returns:
            --------
            edges : Edges
                An edges class/subclass object.
                The collection of edges returned each have the sinkof property of this node (self).
        """
        # return node2of (analogous property)
        return self.node2of(time)


    def nodeof(self, time=None):
        """
            A method of Node.

            Parameter(s):
            -------------
            time : Integer
                Time to check connectivity.

            Returns:
            --------
            edges : Edges
                An edges class/subclass object.
                The collection of edges returned each have the node1 or node2 property of this node (self).
        """
        # if time was specified.
        if time is not None:
            # get all graph edges that are active at this time.
            edges = self.graph.edges.get_active_edges(time)
        else:
            # no time was specified, get all the graph's edges.
            edges = self.graph.edges
        # return the edges that have this node as their 'node1' or 'node2' property.
        return edges.get_edge_by_node(self.label)


    def neighbours(self, time=None):
        """
            A method of Node.

            Parameter(s):
            -------------
            time : Integer
                Time to check connectivity.

            Returns:
            --------
            nodes : Nodes
                A nodes class/subclass object.
                The collection of nodes returned that are adjacent to this node (self).
        """
        node1_edges = self.node1of(time) # edges that have this node as their 'node1' property.
        node2_edges = self.node2of(time) # edges that have this node as their 'node2' property.
        # create a new nodes collection.
        neighbours = self.graph.nodes.subset([])
        # for each edge in the node1 edges.
        for edge in node1_edges.set:
            # if the node has not already been added.
            if not neighbours.exists(edge.node2.label):
                # add the node as a neighbour.
                neighbours.add(edge.node2.label)
        # for each edge in the node2 edges.
        for edge in node2_edges.set:
            # if the node has not already been added.
            if not neighbours.exists(edge.node1.label):
                # add the node as a neighbour.
                neighbours.add(edge.node1.label)
        return neighbours



class ForemostNode(Node):
    """
        A class to represent a node on a graph.

        Parameter(s):
        -------------
        label : String
            A label for the node.
        graph : Graph
            A valid Graph class/subclass.
        time : Integer
            A foremost time. Defaults to infinity (unreachable).

        Object Propertie(s):
        --------------------
        label : String
            Inherited from Node.
        graph : Graph
            Inherited from Node.
        data : Dictionary
            Inherited from Node.
        time : Integer
            The node's foremost time.

        See also:
        ---------
            Node
            Nodes
            ForemostNodes
    """

    def __init__(self, label, graph, time=float('inf')):
        super().__init__(label, graph)
        self.time = time
        self.data['foremost_time'] = time


    def print(self):
        """
            A method of ForemostNode.

            Returns:
            --------
                None, prints the label of the node and the foremost time.
        """
        print(self.label, self.time)



class Nodes:
    """
        A class to represent a collection of nodes on a graph.

        Parameter(s):
        -------------
        graph : Graph
            A valid Graph class/subclass.


        Object Propertie(s):
        --------------------
        set : Set
            The set of nodes.
        graph : Graph
            The graph of which the nodes collection belongs to.


        See also:
        ---------
            Node
            ForemostNode
            ForemostNodes
    """
    def __init__(self, graph):
        self.set = set() # unorderd, unindexed, unique collection of node objects
        self.graph = graph


    def aslist(self):
        """
            A method of Nodes.

            Returns:
            --------
            nodes : List
                A list of the nodes.
        """
        return list(self.set)


    def add(self, label):
        """
            A method of Nodes.

            Parameter(s):
            -------------
            label : String
                The label of the node to be added.

            Returns:
            --------
            node : Node
                The corresponding node object.
        """
        # check if a node with this label already exists in the graph.
        if not self.exists(str(label)):
            # if it does not, add it (create a new node object).
            self.set.add(Node(label, self.graph))
        # return the node object (get or create).
        return self.get(label)


    def remove(self, label):
        """
            A method of Nodes.

            Parameter(s):
            -------------
            label : String
                The label of the node to be removed.

            Returns:
            --------
            Result : Boolean
                Removes the node if it exists in the graph.
        """
        # check if a node with this label already exists in the graph.
        if not self.exists(str(label)):
            print('Error: Node {} not found in graph {}.'.format(label, self.graph.label))
            return False
        else:
            self.set.remove(self.get(label))
            print('Node {} removed from graph {}.'.format(label, self.graph.label))
            return True


    def subset(self, alist):
        """
            A method of Nodes.

            Parameter(s):
            -------------
            alist : List
                A list of node objects.

            Returns:
            --------
            subset : Nodes
                A nodes collection.
            
        """
        # create a new nodes collection subset.
        subset = self.__class__(self.graph)
        # for each node in the specified list.
        for node in alist:
            # add the node to the subset.
            subset.set.add(node)
        # return the new collection of nodes.
        return subset


    def get(self, label):
        """
            A method of Nodes.

            Parameter(s):
            -------------
            label : String
                The label of the node to be searched for.

            Returns:
            --------
            node : Node
                The node in the collection with label 'label' (if it exists).
            
        """
        return next((node for node in self.set if node.label == label), None)


    def exists(self, label):
        """
            A method of Nodes.

            Parameter(s):
            -------------
            label : String
                The label of the node to be checked for.

            Returns:
            --------
            exists : Boolean
                True/false depending of whether node with label 'label' exists in the collection.
            
        """
        return True if self.get(label) is not None else False

    
    def count(self):
        """
            A method of Nodes.

            Returns:
            --------
            count : Integer
                The number of nodes in the collection.
            
        """
        return len(self.set)


    def labels(self):
        """
            A method of Nodes.

            Returns:
            --------
            labels : List
                A list of node labels in the collection.
            
        """
        return [node.label for node in self.set]


    def print(self):
        """
            A method of Nodes.

            Returns:
            --------
                None, calls print for each node in the collection.
        """
        print('Nodes:')
        for node in self.set:
            node.print()


    def add_data(self, csv_path):
        """
            A method of Nodes.

            Parameter(s):
            -------------
            csv_path : String
                The path of the csv file.

            Returns:
            --------
                None, adds the data in the csv data frame to each node.
                The csv data must correspond to the nodes in the node collection.
        """
        # create a data frame from the csv file.
        data_frame = pd.read_csv(csv_path)
        # for each row in the data frame.
        for index, row in data_frame.iterrows():
            # if a 'label' column exists.
            if self.exists(row['label']):
                # get the node corresponding to that 'label'.
                node = self.get(row['label'])
                # for each column, add the data to this node.
                for col in data_frame.columns:
                    node.data[col] = row[col]



class ForemostNodes(Nodes):
    """
        A class to represent a collection of foremost nodes on a tree.
        Inherits properties & methods from Nodes.

        Parameter(s):
        -------------
        graph : Graph
            A valid Graph class/subclass.

        Object Propertie(s):
        --------------------
        set : Set
            Inherited from Nodes.
        graph : Graph
            Inherited from Nodes.

        See also:
        ---------
            Node
            Nodes
            ForemostNodes
    """

    def __init__(self, graph):
        super().__init__(graph)


    def add(self, label, time=float('inf')):
        """
            A method of ForemostNodes.

            Parameter(s):
            -------------
            label : String
                The label of the node to be added.
            time : Integer
                A foremost time. Defaults to infinity (unreachable).

            Returns:
            --------
            node : Node
                The corresponding node object.
        """
        # check if a node with this label already exists in the graph.
        if not self.exists(str(label)):
            # if it does not, add it (create a new node object).
            self.set.add(ForemostNode(label, self.graph, time))
        # return the node object (get or create).
        return self.get(label)


    def times(self):
        """
            A method of ForemostNodes.

            Returns:
            --------
            times : List
                A list of node times in the collection.
        """
        return [node.time for node in self.set]


    def get_reachable(self):
        """
            A method of ForemostNodes.

            Returns:
            --------
            subset : ForemostNodes
                A subset of reachable nodes in the collection.
        """
        return self.subset([node for node in self.set if not math.isinf(node.time)])
