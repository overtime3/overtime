"""
Algorithms for computing temporal PageRank scores from temporal graph objects
"""


def temporal_pagerank(graph, alpha=0.85, beta=0.5, t=None, intervals=None):
    """
        Returns the temporal PageRank score of nodes in a directed temporal graph.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            An directed temporal graph.
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
            closeness_values = temporal_pagerank(graph, alpha=0.85, beta=1.0, t=16, intervals=((1, 5), (8, 10)))

        Notes:
        ------
        This implementation for calculating temporal PageRank scores utilizes an algorithm outlined in "Temporal
        Pagerank" (Rozenshtein & Gionis, 2016), found here:
        https://link.springer.com/chapter/10.1007/978-3-319-46227-1_42. Their algorithm takes as input a temporal graph
        (rather than, say, a static expansion) and returns the temporal PageRank score of all nodes in a graph. It
        is based on the random walk interpretation of PageRank with temporal information incorporated. PageRank scores
        depend on the time input to the algorithm, and as such the relative order of PageRank scores changes over time
        reflecting "concept drift", where the importance of a node may change in a temporal network with increasing
        time.

        TODO:
        -----
        - Implement some kind of parameter to cause function to return evolving values over time
        - Test validity on dummy data + debug
        - Test with bigger datasets, e.g. those included in overtime + debug
        - Write unit tests
    """

    # Restrict graph to specified time interval
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)

    if t is None:
        t = graph.edges.end()

    # Initialize
    pagerank = {node: 0 for node in graph.nodes.labels()}
    active_walks = {node: 0 for node in graph.nodes.labels()}

    # Iterate over edge stream
    for edge in graph.edges.set:

        if edge.start > t:
            break

        u = edge.node1.label
        v = edge.node2.label

        pagerank[u] += (1 - alpha)
        active_walks[u] += (1 - alpha)
        pagerank[v] += active_walks[u] * alpha

        if 0 < beta < 1:
            active_walks[v] += active_walks[u] * (1 - beta) * alpha
            active_walks[u] *= beta

        elif beta == 1:
            active_walks[v] += active_walks[u] * alpha
            active_walks[u] = 0

    return pagerank
