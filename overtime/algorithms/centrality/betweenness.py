"""
Algorithms for computing temporal betweenness centrality for temporal graph objects.
"""


def temporal_betweenness(graph, optimality="shortest", intervals=None, normalize=False, add_data=False):
    """
        Returns the betweenness centralities of nodes in a temporal graph.

        Parameter(s):
        -------------
        graph : TemporalGraph
            A temporal graph.
        optimality : string
            Concept of optimal path in a temporal graph to be used. Can be "shortest" or "foremost".
        intervals : tuple/List
            A tuple of intervals (pairs of start and end times) for the temporal graph to be restricted to.
            Example: ((0,3), (5,7))
        normalize : bool
            Whether to apply normalization to the produced centrality values.
        add_data : bool
            Whether to add the centrality values to the data attributes of the nodes in the nodes collection.

        Returns:
        --------
        betweeness_centrality : dict
            The temporal betweenness centrality of the nodes.
            For example: {A: 12.0, B: 1.2, C: 2.5...}

        Example(s):
        -----------
            graph = TemporalGraph('test_network', data=CsvInput('./network.csv'))
            betweenness_values = betweenness_centrality(graph, optimality="fastest", intervals=((1, 5), (8, 10)))

        Notes:
        ------
        This implementation for calculating fastest temporal path durations is based on an algorithm detailed in
        "Algorithmic Aspects of Temporal Betweenness" (Buß et al. 2020), found here: https://arxiv.org/pdf/2006.08668.pdf.
        Their algorithm takes as input a temporal graph (rather than, say, a static expansion) and returns the temporal
        betweenness centrality of all nodes in the graph. Temporal betweenness centrality can be based on multiple
        notions of optimal path, and as such this algorithm can be executed using either the "shortest" or
        "shortest-foremost" notions of optimal path as outlined in Buß et al. (2020). Normalization is applied as seen in
        "Temporal Node Centrality in Complex Networks" (Kim and Anderson, 2011), found here:
        https://www.cl.cam.ac.uk/~rja14/Papers/TemporalCentrality.pdf.

    """
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)  # restrict graph to specified time interval

    labels = graph.nodes.labels()

    # Algorithm starts
    shortest_centrality = {node: 0 for node in labels}
    foremost_centrality = {node: 0 for node in labels}

    for s in labels:

        # Initialize for nodes
        dist_v = {node: -1 for node in labels}
        sigma_v = {node: 0 for node in labels}
        t_min_v = {node: -1 for node in labels}

        # Initialize for node appearances
        node_appearances = [(node, t) for node in labels for t in range(graph.edges.end())]

        delta_v_t_shortest = {v_t: 0 for v_t in node_appearances}
        delta_v_t_foremost = {v_t: 0 for v_t in node_appearances}
        sigma_v_t = {v_t: 0 for v_t in node_appearances}
        paths_v_t = {v_t: [] for v_t in node_appearances}
        dist_v_t = {v_t: -1 for v_t in node_appearances}

        # Initialize values for current source node
        dist_v[s] = 0
        dist_v_t[(s, 0)] = 0
        t_min_v[s] = 0
        sigma_v[s] = 1
        sigma_v_t[(s, 0)] = 1

        # Initialize stack and queue
        S = []          # LIFO -- Stack
        Q = [(s, 0)]    # FIFO -- Queue

        while Q:
            v, t = Q.pop(0)

            # Iterate over temporal neighbours
            for w, t_ in [neighbour for neighbour in graph.nodes.get(v).temporal_neighbours() if t <= neighbour[1]]:

                # For first visit to (w, t_)
                if dist_v_t[(w, t_)] == -1:
                    dist_v_t[(w, t_)] = dist_v_t[(v, t)] + 1
                    if dist_v[w] == -1:       # Shortest path to w
                        dist_v[w] = dist_v_t[(v, t)] + 1

                    S.append((w, t_))
                    Q.append((w, t_))

                if dist_v_t[(w, t_)] == dist_v_t[(v, t)] + 1:   # Shortest path to (w, t_) via (v, t)
                    sigma_v_t[(w, t_)] += sigma_v_t[(v, t)]
                    paths_v_t[(w, t_)].append((v, t))
                    if dist_v_t[(w, t_)] == dist_v[w]:          # Shortest path to (w) via (v, t)
                        sigma_v[w] += sigma_v_t[(v, t)]

                if t_min_v[w] == -1 or t_ < t_min_v[w]:         # Shortest-foremost path to (w)
                    t_min_v[w] = t_


        shortest_centrality[s] = shortest_centrality[s] - len([i for i in dist_v.values() if i >= 0]) + 1
        foremost_centrality[s] = foremost_centrality[s] - len([i for i in dist_v.values() if i >= 0]) + 1

        while S:

            w, t_ = S.pop(-1)       # Node appearances in order of decreasing distance from source (s)

            if dist_v_t[(w, t_)] == dist_v[w]:      # Shortest path to (w)
                delta_v_t_shortest[(w, t_)] += (sigma_v_t[(w, t_)] / sigma_v[w])

            if t_ == t_min_v[w]:                    # Shortest-foremost path to (w)
                delta_v_t_foremost[(w, t_)] += 1

            # Dependency accumulation
            for v, t in paths_v_t[(w, t_)]:

                # Shortest notion of optimality
                delta_v_t_shortest[(v, t)] += (sigma_v_t[(v, t)] / sigma_v_t[(w, t_)]) * delta_v_t_shortest[(w, t_)]
                shortest_centrality[v] += (sigma_v_t[(v, t)] / sigma_v_t[(w, t_)]) * delta_v_t_shortest[(w, t_)]

                # Foremost notion of optimality
                delta_v_t_foremost[(v, t)] += (sigma_v_t[(v, t)] / sigma_v_t[(w, t_)]) * delta_v_t_foremost[(w, t_)]
                foremost_centrality[v] += (sigma_v_t[(v, t)] / sigma_v_t[(w, t_)]) * delta_v_t_foremost[(w, t_)]

    # Apply normalization
    if normalize:
        normalization_factor = ((graph.nodes.count() - 1) * (graph.nodes.count() - 2) * (graph.edges.end() - graph.edges.start()))
        shortest_centrality = {label: value / normalization_factor for label, value in shortest_centrality.items()}
        foremost_centrality = {label: value / normalization_factor for label, value in foremost_centrality.items()}

    # Add data to nodes
    if add_data:
        if optimality == "shortest":
            for node in graph.nodes.set:
                node.data["betweenness"] = shortest_centrality[node.label]
        elif optimality == "foremost":
            for node in graph.nodes.set:
                node.data["betweenness"] = foremost_centrality[node.label]

    # Return statement
    if optimality == "shortest":
        return shortest_centrality
    elif optimality == "foremost":
        return foremost_centrality
