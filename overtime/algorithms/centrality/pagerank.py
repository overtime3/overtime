"""
Algorithms for computing temporal PageRank scores from temporal graph objects
"""


def temporal_pagerank(graph, alpha=0.85, beta=0.5, intervals=None):
    """
        Returns the temporal PageRank score of nodes in a directed temporal graph.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            A directed temporal graph.
        alpha : float
            Damping factor; probability of intitiating new walk from current node.
        beta : float (0, 1]
            Transition probability.
        intervals : tuple/List
            A tuple of intervals (pairs of start and end times) for the temporal graph to be restricted to.
            Example: ((0,3), (5,7))
        t : int
            A timepoint in the network for the PageRank calculation to end at.

        Returns:
        --------
        pagerank : dict
            The PageRank score of each node.
            For example: {A: 0.15, B: 0.19, C: 1.41, ...}

        Example(s):
        -----------
            graph = TemporalGraph('test_network', data=CsvInput('./network.csv'))
            pagerank_values = temporal_pagerank(graph, alpha=0.85, beta=1.0, t=16, intervals=((1, 5), (8, 10)))

        Notes:
        ------
        This implementation for calculating temporal PageRank scores utilizes an algorithm outlined in "Temporal
        Pagerank" (Rozenshtein & Gionis, 2016), found here:
        https://link.springer.com/chapter/10.1007/978-3-319-46227-1_42. Their algorithm takes as input a temporal graph
        (rather than, say, a static expansion) and returns the temporal PageRank score of all nodes in a graph across time. 
        It is based on the random walk interpretation of PageRank with temporal information incorporated. PageRank scores
        depend on the time input to the algorithm, and as such the relative order of PageRank scores changes over time
        reflecting "concept drift", where the importance of a node may change in a temporal network with increasing
        time.

    """

    if not graph.directed:
        raise TypeError("You have input an undirected graph. This implementation of PageRank is only defined for "
                        "directed graphs.")

    # Restrict graph to specified time interval
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)

    # Initialize
    pagerank = {node: [0] * graph.edges.end() for node in graph.nodes.labels()}
    active_walks = {node: [0] * graph.edges.end() for node in graph.nodes.labels()}

    # Iterate over edge stream
    for edge in graph.edges.set:

        u = edge.node1.label
        v = edge.node2.label
        t = edge.start - 1      # For indexing in the temporal graph model - graphs start at time 1

        pagerank[u][t] += (1 - alpha)
        active_walks[u][t] += (1 - alpha)
        pagerank[v][t] += active_walks[u][t] * alpha

        if 0 < beta < 1:
            active_walks[v][t] += active_walks[u][t] * (1 - beta) * alpha
            active_walks[u][t] *= beta

        elif beta == 1:
            active_walks[v][t] += active_walks[u][t] * alpha
            active_walks[u][t] = 0

    return pagerank
