
from overtime.components.trees import ForemostTree



def calculate_foremost_tree(graph, root):
    """
        A method which returns the foremost tree for a specified root.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            A directed, temporal graph.
        root : String
            The label of a node.

        Returns:
        --------
        tree : ForemostTree
            A directed, temporal tree with root 'root'.

        Example(s):
        -----------
            graph = TemporalDiGraph('test_network', data=CsvInput('./network.csv'))
            foremost_a = calculate_foremost_tree(graph, 'a')

        See also:
        ---------
            calculate_reachability
    """

    # check if the specified root actually exists in the graph.
    if not graph.nodes.exists(root):
        print('Error: ' + str(root) + ' does not exist in this graph.')
        return None

    timespan = graph.edges.timespan() # graph timespan.
    start = timespan[0] # start time.
    end = timespan[-1] # end time.

    # initialize the foremost tree object.
    tree = ForemostTree(graph.label, root, start)

    # add each node in the graph to the foremost tree.
    # nodes in the foremost tree are of type ForemostNode and include a time property,
    # which initializes at inf.
    for node in graph.nodes.set:
        tree.nodes.add(node.label)

    # foremost path algorithm:
    # for every edge in the graph edges set (ordered by edge duration start times).
    for edge in graph.edges.set:
        departure = tree.nodes.get(edge.source.label) # departure node of edge
        destination = tree.nodes.get(edge.sink.label) # destination node of edge

        # if edge's duration end is less than or equal to the end time of the graph's timespan
        # and edge's duration start is greater than or equal to the departure node's foremost time.
        # else if edge's duration start is greater than or equal to the end time of the graph's timespan.
        if edge.end <= end and edge.start >= departure.time:
            # if edge's time duration end is less than the destination node's foremost time.
            if edge.end < destination.time:
                # add this edge to the foremost tree.
                tree.edges.add(edge.source.label, edge.sink.label, tree.nodes, edge.start, edge.end)
                # update the destination node's foremost time.
                destination.time = edge.end
                # update the destination node's data.
                destination.data['foremost_time'] = edge.end
        elif edge.start >= end:
            # stop the algorithm.
            break

    # return the resulting foremost tree.
    return tree
