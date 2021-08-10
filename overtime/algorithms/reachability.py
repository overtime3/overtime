
from overtime.algorithms.foremost import calculate_foremost_tree



def calculate_reachability(graph, root):
    """
        A method which returns the reachability of a root in the graph.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            A directed, temporal graph.
        root : String
            The label of a node.

        Returns:
        --------
        reachability : Integer
            The number of reachable nodes from the root node.

        Example(s):
        -----------
            graph = TemporalDiGraph('test_network', data=CsvInput('./network.csv'))
            reachability_a = calculate_reachability(graph, 'a')

        See also:
        ---------
            calculate_foremost_tree
    """

    # check if the specified root actually exists in the graph.
    if not graph.nodes.exists(root):
        print('Error: ' + str(root) + ' does not exist in this graph.')
        return None

    # calculate the foremost tree of the root node.
    tree = calculate_foremost_tree(graph, root)
    # get the root node object in the graph.
    root_node = graph.nodes.get(root)
    # update the root node's data.
    root_node.data['reachability'] = tree.nodes.get_reachable().count()
    # return the reachable node count.
    return root_node.data['reachability']
