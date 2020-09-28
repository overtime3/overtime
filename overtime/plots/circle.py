
import math
from random import shuffle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from overtime.plots.plot import Plot
from overtime.plots.utils import vector_angle, bezier, circle_label_angle



class CircleNode():
    """
        A class to represent a node on a circle plot.

        Parameter(s):
        -------------
        node : Node
            A valid Node object, such as Node().
        index : Integer
            The index of the node on the plot.
        x : Float
            The x coordinate of the node.
        y : Float
            The y coordinate of the node.
        
        Object Propertie(s):
        --------------------
        node : Node
            The corresponding node object in the graph.
        label : String
            The label of the node on the plot.
        index : Integer
            The index of the node on the plot.
        x : Float
            The x coordinate of the node.
        y : Float
            The y coordinate of the node.
        avg : Float
            The combined average vector angle of the node and it's neighbours.
        color : String
            The color of the node on the plot.

        See also:
        ---------
            CircleEdge
            Circle
    """

    def __init__(self, node, index, x=0, y=0):
        self.node = node
        self.label = node.label
        self.index = index
        self.x = x
        self.y = y
        self.avg = 0
        self.color = index



class CircleEdge():
    """
        A class to represent an edge on a circle plot.

        Parameter(s):
        -------------
        edge : Edge
            A valid Edge object, such as TemporalEdge().
        p1 : Dict
            The p1 coordinate of the edge, as a dictionary with keys 'x' and 'y'.
        p2 : Dict
            The p2 coordinate of the edge, as a dictionary with keys 'x' and 'y'.
        
        Object Propertie(s):
        --------------------
        edge : Edge
            The corresponding edge object in the graph.
        label : String
            The label of the edge on the plot.
        p1 : Dict
            The p1 coordinate of the edge, as a dictionary with keys 'x' and 'y'.
        p2 : Dict
            The p2 coordinate of the edge, as a dictionary with keys 'x' and 'y'.

        See also:
        ---------
            CircleNode
            Circle
    """

    def __init__(self, edge, p1, p2):
        self.edge = edge
        self.label = edge.uid
        self.p1 = p1
        self.p2 = p2



class Circle(Plot):
    """
        A circle plot with the option of barycenter ordering.

        Class Propertie(s):
        -------------------
        class_name : String
            The name of the class, used for labelling.

        Parameter(s):
        -------------
        graph : Graph
            A valid Graph class/subclass.
        figure : Figure
            A pyplot figure object.
        axis : Axis
            A pyplot axis object.
        title : String
            A custom title for the plot.
        ordered : Boolean
            A switch to enable/disable barycenter ordering of the circle plot nodes.
        slider : Boolean
            Disabled.
        show : Boolean
            Show the plot.
        save : Boolean
            Save the plot.

        Object Propertie(s):
        --------------------
        name : String
            Inherited from Plot.
        graph : Graph
            Inherited from Plot.
        title : String
            Inherited from Plot.
        nodes : List
            Inherited from Plot.
        edges : List
            Inherited from Plot.
        labels : List
            Inherited from Plot.
        figure : Figure
            Inherited from Plot.
        axis : Axis
            Inherited from Plot.
        is_ordered : Boolean
            Inherited from Plot.
        has_slider : Boolean
            Inherited from Plot.
        show : Boolean
            Inherited from Plot.
        save : Boolean
            Inherited from Plot.

        See also:
        ---------
            CircleNode
            CircleEdge
            Plot
            Slice
    """
    class_name = 'circle'

    def __init__(self, graph, figure=None, axis=None, title=None,
                    ordered=True, slider=False, show=True, save=False):
        super().__init__(graph, figure, axis, title, ordered, False, show, save)


    def create_nodes(self):
        """
            A method of Circle.
            Returns:
            --------
                None, creates the CircleNode objects and optionally applies ordering.
        """
        n = self.graph.nodes.count() # number of nodes in the graph.
        i = 0
        # for each node.
        for node in self.graph.nodes.set:
            x = math.cos(2 * math.pi * i / n) # assign x coordinate based on index around the circle.
            y = math.sin(2 * math.pi * i / n) # assign y coordinate based on index around the circle.
            # create a CircleNode and add it to the nodes list.
            self.nodes.append(CircleNode(node, i, x, y))
            i += 1
        if self.is_ordered:
            # apply barycenter ordering.
            self.order_nodes(self.graph.edges.count())


    def get_node(self, label):
        """
            A method of Circle.

            Parameter(s):
            -------------
                label : String
                    The label of a node.

            Returns:
            --------
                The Circle node object corresponding to the label specified.
        """
        # return (if found) the node in self.nodes whose label equals 'label'.
        return next((node for node in self.nodes if node.label == label), None)


    def order_nodes(self, iterations):
        """
            A method of Circle.

            Parameter(s):
            -------------
                interations : Integer
                    The number of iterations for ordering.

            Returns:
            --------
                None, iteratively updates the positions of the plot's nodes.
        """
        for x in range(iterations):
            # sort the nodes by the combined average position of the node and it's neighbours.
            self.nodes = sorted(self.nodes, key=lambda x:x.avg, reverse=False)
            n = self.graph.nodes.count() # number of nodes in the graph.
            i = 0
            # for each node.
            for node in self.nodes:
                # if the node's index position has changed due to sorting.
                if not node.index == i:
                    # update the node's index to the new one.
                    node.index = i
                    # update the node's x & y values.
                    node.x = math.cos(2 * math.pi * i / n)
                    node.y = math.sin(2 * math.pi * i / n)
                sum_x = node.x # start the x sum.
                sum_y = node.y # start the y sum.
                # for each of the nodes neighbours.
                for neighbour in node.node.neighbours().set:
                    # append the x value of the neighbour to the x sum.
                    sum_x = sum_x + self.get_node(neighbour.label).x
                    # append the y value of the neighbour to the y sum.
                    sum_y = sum_y + self.get_node(neighbour.label).y
                # calculate the average vector angle of the node and it's neighbours and update.
                node.avg = vector_angle(sum_x, sum_y)
                i += 1


    def create_edges(self):
        """
            A method of Plot/Circle.

            Returns:
            --------
                None, creates the CircleEdge objects.
        """
        # if graph is temporal, create edges in reverse order of time.
        # this will put earliest time labels on top when drawing.
        if not self.graph.static:
            graph_edges = sorted(self.graph.edges.set, key=lambda x:x.start, reverse=True)
        else:
            graph_edges = self.graph.edges.set
        # for each edge in the graph.
        for edge in graph_edges:
            # get p1 from edge's node's positions.
            p1 = {'x': self.get_node(edge.node1.label).x, 'y': self.get_node(edge.node1.label).y}
            # get p2 from edge's node's positions.
            p2 = {'x': self.get_node(edge.node2.label).x, 'y': self.get_node(edge.node2.label).y}
            # create a CircleEdge and add it to the edges list.
            self.edges.append(CircleEdge(edge, p1, p2))
            

    def draw_nodes(self):
        """
            A method of Plot/Circle.

            Returns:
            --------
                None, draws the nodes of the plot.
        """
        n = self.graph.nodes.count() # number of nodes in the graph.
        pos = {}
        pos['x'] = [node.x for node in self.nodes] # x coordinates of every node.
        pos['y'] = [node.y for node in self.nodes] # y coordinates of every node.
        colors = [x for x in range(0, n)] # colors index for every node.
        cmap = self.set3colormap(n) # color map with enough colors for n nodes.
        # draw the nodes using pyplot scatter.
        ax_node = self.axis.scatter(
            pos['x'], pos['y'], s=500, c=colors, cmap=cmap, alpha=0.5, zorder=1
        )
        plt.draw()
        i = 0
        # for every node.
        for node in self.nodes:
            # check what color the node was assigned and update.
            node.color = ax_node.to_rgba(colors[i])
            # draw the node's label, with smart rotation.
            self.axis.text(
                node.x, node.y,
                node.label, color='midnightblue',
                rotation=circle_label_angle(node.x, node.y),
                ha='center', va='center',
                fontsize='x-small',
            )
            i += 1


    def draw_edges(self):
        """
            A method of Plot/Circle.

            Returns:
            --------
                None, draws the edges of the plot.
        """
        # for every edge in the graph.
        for edge in self.edges:
            # assign the same color as node1 of the edge.
            edge_color = self.get_node(edge.edge.node1.label).color
            # if the edge is directed.
            if edge.edge.directed:
                color=edge_color # assign it the same color as the source node.
            else:
                color='lightgrey' # otherwise, make it light grey.
            bezier_edge = bezier(edge.p1, edge.p2) # create a Bézier curve for the edge.
            # draw the edge.
            self.axis.plot(
                bezier_edge['x'],
                bezier_edge['y'],
                linestyle='-',
                color=color,
                alpha=0.5,
                zorder=0
            )
            # if edge is directed.
            if edge.edge.directed:
                # draw a circle to indicate the source side of the edge.
                self.axis.plot(
                    bezier_edge['x'][6],
                    bezier_edge['y'][6],
                    'o',
                    color=edge_color,
                    alpha = 0.5,
                    zorder=1
                )
            # if the graph is temporal.
            if not self.graph.static:
                # draw the start time of the edge.
                self.axis.text(
                    bezier_edge['x'][9], bezier_edge['y'][9],
                    edge.edge.start, 
                    color='midnightblue', backgroundcolor=edge_color,
                    fontsize='xx-small',
                    horizontalalignment='center',
                    rotation=circle_label_angle(bezier_edge['x'][10], bezier_edge['y'][10]),
                    zorder=1,
                )


    def cleanup(self):
        """
            A method of Plot/Circle.

            Returns:
            --------
                None, updates figure & axis properties & styling.
        """
        # adjust whitespace around the plot.
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0, hspace=0)
        self.remove_xticks(self.axis) # remove x-ticks.
        self.remove_yticks(self.axis) # remove y-ticks.
        self.set_aspect(self.axis) # set aspect ratio.
        self.style_axis(self.axis) # style axis.


    def set_aspect(self, ax):
        """
            A method of Circle.

            Parameter(s):
            -------------
            ax : Axis
                A pyplot axis object.

            Returns:
            --------
                None, updates axis aspect ratio.
        """
        x0, x1 = ax.get_xlim() # get range of x values.
        y0, y1 = ax.get_ylim() # get range of y values.
        ax.set_aspect((x1 - x0) / (y1 - y0)) # update aspect ratio to match x & y ranges.
        ax.margins(0.2, 0.2) # update plot margins.
