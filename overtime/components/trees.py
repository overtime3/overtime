
from overtime.components.digraphs import TemporalDiGraph
from overtime.components.nodes import ForemostNodes
from overtime.components.arcs import TemporalArcs



class ForemostTree(TemporalDiGraph):
    """
        A class which represents a static, undirected graph consisting of nodes and edges.

        Parameter(s):
        -------------
        label : String
            A label for the graph.
        root : String
            The label of the root node.
        start : Integer
            The start time of the root node.

        Object Propertie(s):
        --------------------
        label : String
            Inherited from TemporalDiGraph.
        directed : Boolean
            Inherited from TemporalDiGraph.
        static : Boolean
            Inherited from TemporalDiGraph.
        nodes : Nodes
            A foremost nodes collection representing all nodes in the graph.
        edges : Edges
            An temporal arcs collection representing all edges in the graph.
        root : Node
            The root node of the foremost tree.

        See also:
        ---------
            TemporalGraph
            TemporalDiGraph
    """

    def __init__(self, label, root, start):
        # update the graph label.
        label = label + ' foremost tree [root: ' + root + ']'
        super().__init__(label)
        self.nodes = ForemostNodes(self)
        self.edges = TemporalArcs(self)
        self.root = self.nodes.add(root, start)
