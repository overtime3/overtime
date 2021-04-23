import overtime as ot


def reachable_subtree(graph, root, h):
    """
        A method which returns a subtree for a specified root.
        The reachability of this subtree is h+1.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            A directed, temporal graph.
        root : String
            The name of root.
        h : int
            a threshold, the maximum temporal reachability of the subtree is h+1.

        Returns:
        --------
        tree : ForemostTree
            ForemostTree is an object which represents a static, undirected graph consisting of nodes and edges.
            In this algorithm, it represents a directed, temporal subtree of graph 'graph' with root 'root', and the
            reachability of this subtree is h+1.

    """

    timespan = graph.edges.timespan()  # graph timespan.
    start = timespan[0]  # start time.
    end = timespan[-1]  # end time.

    # initialize the foremost tree object.
    tree = ot.ForemostTree(graph.label, root, start)

    # add each node in the graph to the foremost tree.
    # nodes in the foremost tree are of type ForemostNode and include a time property,
    # which initializes at inf.
    for node in graph.nodes.set:
        tree.nodes.add(node.label)

    # calculate the number of nodes reachable from the root
    accumulator = 0

    # foremost path algorithm:
    # for every edge in the graph edges set (ordered by edge duration start times).
    for edge in graph.edges.set:
        departure = tree.nodes.get(edge.source.label)  # departure node of edge
        destination = tree.nodes.get(edge.sink.label)  # destination node of edge

        # if edge's duration end is less than or equal to the end time of the graph's timespan
        # and edge's duration start is greater than or equal to the departure node's foremost time.
        # else if edge's duration start is greater than or equal to the end time of the graph's timespan.
        if edge.end <= end and edge.start >= departure.time:
            # if edge's time duration end is less than the destination node's foremost time.
            if edge.end < destination.time:
                # add this edge to the foremost tree.
                temp = tree.edges.add(edge.source.label, edge.sink.label, tree.nodes, edge.start, edge.end)
                # update the destination node's foremost time.
                destination.time = edge.end
                # update the destination node's data.
                destination.data['foremost_time'] = edge.end

                # update accumulator
                accumulator += 1
                if accumulator == h:
                    break

        elif edge.start >= end:
            # stop the algorithm.
            break

    # return the resulting foremost tree.
    return tree


def h_approximation(graph, h):
    """
        A h-approximation algorithm to return a set of edges E_ such that (G,λ)\E_ has temporal reachability at most h.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
                A directed, temporal graph.
        h : int
            the maximum permitted temporal reachability.

        Returns:
        --------
        E_ : list
            a set of edges such that (G,λ)\E_ has temporal reachability at most h.

    """

    E_ = []

    # find the node whose temporal reachability is more than h
    while (True):
        root = ''
        for node in graph.nodes.set:
            reachability = ot.calculate_reachability(graph, node.label)
            if reachability > h:
                root = node.label
                break

        # check if the specified root actually exists in the graph.
        if root == '':
            print('The temporal reachability of the input temporal graph is at most h')
            break

        # generate a reachable subtree based on the root
        subtree = reachable_subtree(graph, root, h)

        E_.extend(subtree.edges.uids())
        # update (G, λ) ← (G, λ) \ E_
        for edge in subtree.edges.uids():
            graph.remove_edge(edge)

    return E_

def max_reachability(graph):
    """
        A method to calculate the max temporal reachability of a network.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
                A directed, temporal graph.

        Returns:
        --------
        maxReachability : int
            the max temporal reachability of a network.

    """

    maxReachability = 0

    # check the temporal reachability of each node
    for node in graph.nodes.labels():
        r = ot.calculate_reachability(graph, node)
        if r > maxReachability:
            maxReachability = r

    return maxReachability


def max_endtime(graph):
    """
        A method to calculate the maximum endtime of a network.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
                A directed, temporal graph.

        Returns:
        --------
        maxEndtime : int
            the maximum endtime of a network.

    """

    timespan = graph.edges.timespan()
    maxEndtime = timespan[-1]

    return maxEndtime


def find_edges(graph, layout, j):
    """
        A method to find all the edges that span vj and vj+1.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            A directed, temporal graph.
        layout : list
            The vertices of graph can be arranged in a linear order
            v1,...,vn, called a layout
        j : int
            An indicator which is used to separate the layout of graph into two list,
            v1,...,vj and vj+1,...,vn
            
        Returns:
        --------
        edgeList : list
            a list that contains all the edges that span vj and vj+1.

    """

    edgeList = []
    # divided the layout into two subsets based on j
    layout1 = layout[:j + 1]
    layout2 = layout[j + 1:len(layout)]

    # find all edges with one endpoint in {v1...vj} and one endpoint in {vj+1...vn}
    for edge in graph.edges.set:
        if (edge.sink.label in layout1 and edge.source.label in layout2) or (
                edge.sink.label in layout2 and edge.source.label in layout1):
            edgeList.append(edge.uid)

    return edgeList


def generate_Layout(graph):
    """
        A method to generate a layout of a network, such as {v1, v2, v3， ....， vn}.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
                A directed, temporal graph.

        Returns:
        --------
        layout : list
            a layout of the network.

    """

    # generate a layout based on the order of their labels
    layout = graph.nodes.labels()
    return layout


def c_approximation(graph, h, layout):
    """
        A c-approximation algorithm to return a set of edges E_ such that (G,λ)\E_ has temporal reachability at most h.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
                A directed, temporal graph.
        h : int
            the maximum permitted temporal reachability.
        layout : list
            a layout of the graph, such as {v1, v2, v3， ....， vn}.

        Returns:
        --------
        E_ : list
            a set of edges such that (G,λ)/E_ has temporal reachability at most h.

    """

    # result edge set
    E_ = []

    i = 0

    while (max_reachability(graph) > h):
        start = i
        end = len(layout) - 1
        mid = (start + end) // 2

        # find the maximum j∈{i,...,n}such that the maximum reachability in the
        # subgraph (G[{vi,...,vj}],λ|E(G[{vi,...,vj}])) is at most h
        while (start <= end):

            # the maximum endtime in the graph
            maxEndtime = max_endtime(graph)

            # generate a temporal subgraph with updated timespan and nodes
            subgraph = graph.get_temporal_subgraph(intervals=(0, maxEndtime), nodes=layout[:mid + 1])

            # calculate the maximum reachability in the subgraph
            maxReachability = max_reachability(subgraph)
            if maxReachability > h:
                end = mid - 1
            else:
                start = mid + 1
            mid = (start + end) // 2

        # find edges that span vj,vj+1
        edgeList = find_edges(graph, layout, mid)

        # add all edges that span vj,vj+1 to E_
        E_.extend(edgeList)

        # update (G, λ) ← (G, λ) \ E_
        for edge in edgeList:
            graph.remove_edge(edge)

        i = mid + 1

    print('there is no nodes with reachability more than h')

    return E_
