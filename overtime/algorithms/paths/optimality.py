"""
Various functions for calculating optimal path trees.
"""


def calculate_fastest_path_durations(graph, root, interval=None):
    """
        Returns a dictionary where the keys are node labels and the values are the duration of the shortest path to
        the nodes from a given root. Unreachable nodes have distance set to infinity.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            A directed temporal graph.
        root: string
            The node label for a node to use as root.
        interval : tuple/List
            A time interval.
            For example: ((0,3))

        Returns:
        --------
        fastest_path_durations : dict
            The durations of the fastest paths to all other nodes from the root node.
            For example: {A: 0, B: 2, C: 4, D: inf...}

        Notes:
        ------
        Our implementation for calculating fastest temporal path durations is based on the algorithm as specified in
        "Path Problems in Temporal Graphs" (Wu et al. 2014), found here: https://www.vldb.org/pvldb/vol7/p721-wu.pdf.
        Their algorithm takes as input a temporal graph (rather than, say, a static expansion) and returns the duration
        of the fastest time-respecting paths to all other nodes.

        TODO
        ----
        - Generalize to undirected graphs
        - Perhaps have this function return the actual tree, and another function to calculate the duration of paths
          in that tree

    """
    # If interval not specified, set interval to be entire lifetime of graph
    if not interval:
        interval = (0, graph.edges.end())

    # Initialize lists for storing fastest path start and arrival times to each node
    path_start_end_times = {label: [] for label in graph.nodes.labels()}

    # Initialize dict for storing fastest path duration for each node
    # Root initialized to 0, rest to infinity
    fastest_path_durations = {label: float("inf") for label in graph.nodes.labels()}
    fastest_path_durations[root] = 0

    # Iterate over edge stream representation
    for edge in graph.edges.set:

        u = edge.node1.label
        v = edge.node2.label
        t = edge.start

        if interval[0] < t <= interval[1]:

            # If source node of edge is root
            if u == root:
                if (t, t) not in path_start_end_times[root]:
                    path_start_end_times[root].append([t, t])

            # If path start and arrival times do not yet exist for u, continue
            if not path_start_end_times[u]:
                continue

            # Get best start and new arrival times of path
            # Apparently itemgetter is faster for this - is it worth having an extra dependency?
            new_start_time = max(path_start_end_times[u], key=lambda item: item[1])[0]
            new_arr_time = edge.end

            # Update fastest path arrival time for node v if v already visited
            for element in path_start_end_times[v]:
                if element[0] == new_start_time:
                    element[1] = new_arr_time
                    break
            # If not yet visited, insert new start and arrival time
            else:
                path_start_end_times[v].append([new_start_time, new_arr_time])

            # Remove dominated elements from path_start_end_times -- this is going to be slow, is there a better
            # way?
            for a in path_start_end_times[v]:
                for b in path_start_end_times[v]:
                    if (b[0] > a[0] and b[1] <= a[1]) or (b[0] == a[0] and b[1] < a[1]):
                        break
                    path_start_end_times[v].remove(a)

            # If path faster than currently stored path, update stored duration
            if new_arr_time - new_start_time < fastest_path_durations[v]:
                fastest_path_durations[v] = new_arr_time - new_start_time

    return fastest_path_durations
