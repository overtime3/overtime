import overtime as ot
import copy
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.charts import Page
from pyecharts.charts import Timeline
from overtime.algorithms import edgeDeletion


def echarts_Circular(graph,
                     h,
                     symbol_size=20,
                     line_width=1,
                     width="800px",
                     height="500px",
                     curve_list=[0.1, 0.3],
                     path='circleExample.html',
                     title='Circle_Graph',
                     subtitle='',
                     pageLayout=Page.DraggablePageLayout,
                     show_node_value=True,
                     show_edge_value=True,
                     render=True):
    """
        A method to render a network in circular layout.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            An object which represents a temporal, directed graph consisting of nodes and temporal arcs.
        h : int
            The threshold of temporal reachability. Nodes will be assigned different color based on this value.
        symbol_size : int
            The size of the nodes.
        line_width : int
            The width of the edges.
        width: String
            The width of the image.
            Default value: 800px
        height: String
            The height of the image.
            Decault value: 500px
        curve_list : list
            A list contains one or two values which represent the curvature of edges.
            If you give two values in this list, then duplicate edges (a->b, b->a) will be rendered using different curvature.
            Otherwise, duplicate edges will be rendered using the same curvature.
            Decault value: [0.1, 0.3]
        path : String
            The path of the rendered image.
            Default value: circleExample.html
        title : String
            The title of the rendered image.
            Default value: Circle_Graph
        subtitle : String
            The subtitle of the rendered image.
            Default value: ''
        pageLayout : PageLayoutOpts
            There are two kinds of page layout: Page.DraggablePageLayout and Page.SimplePageLayout.
            In Page.SimplePageLayout, the width and height of the image border is stable.
            While in Page.DraggablePageLayout, the image border can be changed.
            Default value: Page.DraggablePageLayout
        show_node_value : boolean
            Whether show the reachability of nodes.
            Default value: True
        show_edge_value : boolean
            Whether show the start time and end time of edges.
            Default value: True
        render : boolean
            Whether generate the html file directly.
            Default value: True

        Returns:
        --------
        c : Graph
            basic charts object in pyecharts package
    """

    # initialize nodes list
    nodes = []
    if show_node_value:
        for i in range(len(graph.nodes.aslist())):
            # calculate reachability for each nodes
            reachability = ot.calculate_reachability(graph, graph.nodes.labels()[i])
            if reachability > h:
                # nodes with reachability more than h will be assigned category 0
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=0,
                                            value=reachability))
            else:
                # nodes with reachability less than or equal to h will be assigned category 1
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=1,
                                            value=reachability))
    else:
        for i in range(len(graph.nodes.aslist())):
            # calculate reachability for each nodes
            reachability = ot.calculate_reachability(graph, graph.nodes.labels()[i])
            if reachability > h:
                # nodes with reachability more than h will be assigned category 0
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=0))
            else:
                # nodes with reachability less than or equal to h will be assigned category 1
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=1))

    # initialize links list
    links = []
    # used to check duplicate edges
    edge_list = []
    # accumulate the appearance times of each edge
    accumulator = np.zeros(len(graph.edges.labels()))
    if show_edge_value:
        # initialize value list of edges
        edge_value = []
        # 1. compare all edge labels with unique edge labels to find which edges are duplicated
        # 2. edge value of duplicate edges will be added to the same list and shown together
        for i in range(len(graph.edges.labels())):
            for j in range(len(graph.edges.ulabels())):
                if graph.edges.labels()[i] == graph.edges.ulabels()[j]:
                    if j < len(edge_value):
                        edge_value[j].append('{start time: ' + str(graph.edges.start_times()[i]) + ', end time: ' + str(
                            graph.edges.end_times()[i]) + '}')
                    else:
                        tmp_edge_value = []
                        tmp_edge_value.append(
                            '{start time: ' + str(graph.edges.start_times()[i]) + ', end time: ' + str(
                                graph.edges.end_times()[i]) + '}')
                        edge_value.append(tmp_edge_value)
            # print the rate of progress
            print('rate of progress: {}%'.format((i + 1) / len(graph.edges.labels()) * 100))

        # check duplicate edges
        # 1. get nodes' name by spliting the edge labels
        # 2. transform them to set and compare them with elements in 'edge_list'
        # 3. if they are not duplicated, add them to 'edge_list'
        for i in range(len(graph.edges.ulabels())):
            tmp = graph.edges.ulabels()[i].split('-')

            flag = True
            for j in np.arange(0, len(edge_list)):
                if set(tmp) == set(edge_list[j]):
                    accumulator[i] = 1
                    flag = False
                    break;

            if flag:
                edge_list.append(tmp)

            # add links
            # duplicate edges with different direction will be rendered based on their corresponding curvature
            # duplicate edges with the same direction will be rendered only once
            links.append(opts.GraphLink(source=tmp[0],
                                        target=tmp[1],
                                        value=edge_value[i],
                                        linestyle_opts=opts.LineStyleOpts(
                                            curve=curve_list[int(accumulator[i]) % len(curve_list)])

                                        ))
    else:
        # check duplicate edges
        for i in range(len(graph.edges.ulabels())):
            tmp = graph.edges.labels()[i].split('-')

            flag = True
            for j in np.arange(0, len(edge_list)):
                if set(tmp) == set(edge_list[j]):
                    accumulator[i] = 1
                    flag = False
                    break;

            if flag:
                edge_list.append(tmp)

            links.append(opts.GraphLink(source=tmp[0],
                                        target=tmp[1],
                                        linestyle_opts=opts.LineStyleOpts(
                                            curve=curve_list[int(accumulator[i]) % len(curve_list)])

                                        ))

    # initialize categories list
    categories = [
        opts.GraphCategory(name='nodes with reachability more than {}'.format(h)),
        opts.GraphCategory(name='nodes with reachability less than or equal to {}'.format(h))
    ]

    # generate an html file of the graph
    c = (
        Graph(init_opts=opts.InitOpts(width=width, height=height))
            .add(
            "",
            nodes=nodes,
            links=links,
            categories=categories,
            layout="circular",
            is_rotate_label=True,
            symbol_size=symbol_size,
            linestyle_opts=opts.LineStyleOpts(color="source", width=line_width),
            label_opts=opts.LabelOpts(position="right"),
            edge_symbol=['circle', 'arrow'],
            edge_symbol_size=10
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle=subtitle,
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=40),
                                      subtitle_textstyle_opts=opts.TextStyleOpts(font_size=20)),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%",
                                        textstyle_opts=opts.TextStyleOpts(font_size=20)),
        )
    )

    # if render is True, generate an html file
    if render:
        page = Page(layout=pageLayout)
        page.add(c)
        page.render(path)

    return c


def echarts_Force(graph,
                  h,
                  repulsion=500,
                  is_draggable=True,
                  width="1200px",
                  height="600px",
                  path='forceExample.html',
                  title='Force_Graph',
                  subtitle='',
                  pageLayout=Page.SimplePageLayout,
                  show_node_value=True,
                  show_edge_value=True,
                  render=True):
    """
        A method to render a network in force layout.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            An object which represents a temporal, directed graph consisting of nodes and temporal arcs.
        h : int
            The threshold of temporal reachability. Nodes will be assigned different color based on this value.
        repulsion : int
            The repulsion between nodes.
        is_draggable : boolean
            Whether the nodes are moveable.
        width: String
            The width of the image.
            Default value: 1200px
        height: String
            The height of the image.
            Decault value: 600px
        path : String
            The path of the rendered image.
            Default value: forceExample.html
        title : String
            The title of the rendered image.
            Default value: Force_Graph
        subtitle : String
            The subtitle of the rendered image.
            Default value: ''
        pageLayout : PageLayoutOpts
            There are two kinds of page layout: Page.DraggablePageLayout and Page.SimplePageLayout.
            In Page.SimplePageLayout, the width and height of the image border is stable.
            While in Page.DraggablePageLayout, the image border can be changed.
            Default value: Page.SimplePageLayout
        show_node_value : boolean
            Whether to show the reachability of nodes.
            Default value: True
        show_edge_value : boolean
            Whether to show the start time and end time of edges.
            Default value: False
        render : boolean
            Whether to generate the html file directly.
            Default value: True

        Returns:
        --------
        c : Graph
            basic charts object in pyecharts package
    """

    # initialize nodes list
    nodes = []
    if show_node_value:
        for i in range(len(graph.nodes.aslist())):
            # calculate reachability for each nodes
            reachability = ot.calculate_reachability(graph, graph.nodes.labels()[i])
            if reachability > h:
                # nodes with reachability more than h will be assigned category 0
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=0,
                                            value=reachability))
            else:
                # nodes with reachability more than h will be assigned category 1
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=1,
                                            value=reachability))
    else:
        for i in range(len(graph.nodes.aslist())):
            # calculate reachability for each nodes
            reachability = ot.calculate_reachability(graph, graph.nodes.labels()[i])
            if reachability > h:
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=0))
            else:
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=1))
                # initialize links list
    links = []
    # used to check duplicate edges
    edge_list = []
    if show_edge_value:
        # initialize value list of edges
        edge_value = []
        # 1. compare all edge labels with unique edge labels to find which edges are duplicated
        # 2. edge value of duplicate edges will be added to the same list and shown together
        for i in range(len(graph.edges.labels())):
            for j in range(len(graph.edges.ulabels())):
                if graph.edges.labels()[i] == graph.edges.ulabels()[j]:
                    if j < len(edge_value):
                        edge_value[j].append('{start time: ' + str(graph.edges.start_times()[i]) + ', end time: ' + str(
                            graph.edges.end_times()[i]) + '}')
                    else:
                        tmp_edge_value = []
                        tmp_edge_value.append(
                            '{start time: ' + str(graph.edges.start_times()[i]) + ', end time: ' + str(
                                graph.edges.end_times()[i]) + '}')
                        edge_value.append(tmp_edge_value)
            # print the rate of progress
            print('rate of progress: {}%'.format((i + 1) / len(graph.edges.labels()) * 100))

        for i in range(len(graph.edges.ulabels())):
            tmp = graph.edges.ulabels()[i].split('-')
            links.append(opts.GraphLink(source=tmp[0],
                                        target=tmp[1],
                                        value=edge_value[i]
                                        )
                         )
    else:
        for i in range(len(graph.edges.ulabels())):
            tmp = graph.edges.ulabels()[i].split('-')
            links.append(opts.GraphLink(source=tmp[0],
                                        target=tmp[1]
                                        )

                         )

    # initialize categories list
    categories = [
        opts.GraphCategory(name='nodes with reachability more than {}'.format(h)),
        opts.GraphCategory(name='nodes with reachability less than or equal to {}'.format(h))
    ]

    # generate an html file of the graph
    c = (
        Graph(init_opts=opts.InitOpts(width=width, height=height))
            .add(
            "",
            nodes=nodes,
            links=links,
            categories=categories,
            layout="force",
            is_draggable=is_draggable,
            repulsion=500,
            is_rotate_label=True,
            symbol_size=20,
            linestyle_opts=opts.LineStyleOpts(color="source", width=1),
            label_opts=opts.LabelOpts(position="right"),
            edge_symbol=['circle', 'arrow'],
            edge_symbol_size=10
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle=subtitle,
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=40),
                                      subtitle_textstyle_opts=opts.TextStyleOpts(font_size=20)),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%",
                                        textstyle_opts=opts.TextStyleOpts(font_size=20)),
        )
    )

    if render:
        page = Page(layout=pageLayout)
        page.add(c)
        page.render(path)

    return c


def echarts_Location(graph,
                     h,
                     x,
                     y,
                     symbol_size=5,
                     line_width=1,
                     width="1400px",
                     height="800px",
                     path='locationExample.html',
                     title='Location_Graph',
                     subtitle='',
                     showName=True,
                     font_size=15,
                     edge_symbol_size=10,
                     pageLayout=Page.SimplePageLayout,
                     show_node_value=True,
                     show_edge_value=True,
                     render=True):
    """
        A method to render a network in location layout.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            An object which represents a temporal, directed graph consisting of nodes and temporal arcs.
        h : int
            The threshold of temporal reachability. Nodes will be assigned different color based on this value.
        x : String
            The name of the x coordinates of the nodes.
            For example, in the network of London subway stations, the name of x coordinate can be 'lon' or 'lat'.
        y : String
            The name of the y coordinates of the nodes.
            For example, in the network of London subway stations, the name of x coordinate can be 'lon' or 'lat'.
        symbol_size : int
            The size of the nodes.
        line_width : int
            The width of the edges.
        width: String
            The width of the image.
            Default value: 1200px
        height: String
            The height of the image.
            Decault value: 600px
        path : String
            The path of the rendered image.
            Default value: forceExample.html
        title : String
            The title of the rendered image.
            Default value: Location_Graph
        subtitle : String
            The subtitle of the rendered image.
            Default value: ''
        showName : boolean
            Whether to show the name of nodes.
            Default value: True
        font_size : int
            The font size of the value on the nodes.
            Default value: 10
        edge_symbol_size : int
            The size of the symbol on the edges.
            Default value: 10
        pageLayout : PageLayoutOpts
            There are two kinds of page layout: Page.DraggablePageLayout and Page.SimplePageLayout.
            In Page.SimplePageLayout, the width and height of the image border is stable.
            While in Page.DraggablePageLayout, the image border can be changed.
            Default value: Page.SimplePageLayout
        show_node_value : boolean
            Whether to show the reachability of nodes.
            Default value: True
        show_edge_value : boolean
            Whether to show the start time and end time of edges.
            Default value: False
        render : boolean
            Whether to generate the html file directly.
            Default value: True

        Returns:
        --------
        c : Graph
            basic charts object in pyecharts package
    """

    # initialize nodes list
    nodes = []
    if show_node_value:
        for i in range(len(graph.nodes.aslist())):
            # calculate reachability for each nodes
            reachability = ot.calculate_reachability(graph, graph.nodes.labels()[i])
            if reachability > h:
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=0,
                                            x=graph.nodes.aslist()[i].data[x],
                                            y=graph.nodes.aslist()[i].data[y],
                                            label_opts=opts.LabelOpts(is_show=showName, font_size=font_size),
                                            value=reachability

                                            ))
            else:
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=1,
                                            x=graph.nodes.aslist()[i].data[x],
                                            y=graph.nodes.aslist()[i].data[y],
                                            label_opts=opts.LabelOpts(is_show=showName, font_size=font_size),
                                            value=reachability
                                            ))
    else:
        for i in range(len(graph.nodes.aslist())):
            # calculate reachability for each nodes
            reachability = ot.calculate_reachability(graph, graph.nodes.labels()[i])
            if reachability > h:
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=0,
                                            x=graph.nodes.aslist()[i].data[x],
                                            y=graph.nodes.aslist()[i].data[y],
                                            label_opts=opts.LabelOpts(is_show=showName, font_size=font_size)

                                            ))
            else:
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=1,
                                            x=graph.nodes.aslist()[i].data[x],
                                            y=graph.nodes.aslist()[i].data[y],
                                            label_opts=opts.LabelOpts(is_show=showName, font_size=font_size)

                                            ))

    # initialize links list
    links = []
    if show_edge_value:
        # initialize value list of edges
        edge_value = []
        # 1. compare all edge labels with unique edge labels to find which edges are duplicated
        # 2. edge value of duplicate edges will be added to the same list and shown together
        for i in range(len(graph.edges.labels())):
            for j in range(len(graph.edges.ulabels())):
                if graph.edges.labels()[i] == graph.edges.ulabels()[j]:
                    if j < len(edge_value):
                        edge_value[j].append('{start time: ' + str(graph.edges.start_times()[i]) + ', end time: ' + str(
                            graph.edges.end_times()[i]) + '}')
                    else:
                        tmp_edge_value = []
                        tmp_edge_value.append(
                            '{start time: ' + str(graph.edges.start_times()[i]) + ', end time: ' + str(
                                graph.edges.end_times()[i]) + '}')
                        edge_value.append(tmp_edge_value)
            # print the rate of progress
            print('rate of progress: {}%'.format((i + 1) / len(graph.edges.labels()) * 100))

        for i in range(len(graph.edges.ulabels())):
            tmp = graph.edges.ulabels()[i].split('-')

            links.append(opts.GraphLink(source=tmp[0],
                                        target=tmp[1],
                                        value=edge_value[i]

                                        ))

    else:
        for i in range(len(graph.edges.ulabels())):
            tmp = graph.edges.ulabels()[i].split('-')

            links.append(opts.GraphLink(source=tmp[0],
                                        target=tmp[1]

                                        ))

    # initialize categories list
    categories = [
        opts.GraphCategory(name='nodes with reachability more than {}'.format(h)),
        opts.GraphCategory(name='nodes with reachability less than or equal to {}'.format(h))
    ]

    # generate an html file of the graph
    c = (
        Graph(init_opts=opts.InitOpts(width=width, height=height))
            .add(
            "",
            nodes=nodes,
            links=links,
            categories=categories,
            layout="none",
            symbol_size=symbol_size,
            linestyle_opts=opts.LineStyleOpts(is_show=True, curve=0.1, width=line_width),
            label_opts=opts.LabelOpts(position="right"),
            edge_symbol=['circle', 'arrow'],
            edge_symbol_size=symbol_size
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle=subtitle,
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=40),
                                      subtitle_textstyle_opts=opts.TextStyleOpts(font_size=20)),
            legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%",
                                        textstyle_opts=opts.TextStyleOpts(font_size=20)),
        )
    )

    if render:
        page = Page(layout=pageLayout)
        page.add(c)
        page.render(path)

    return c


def echarts_Timeline(graph,
                     h,
                     x='',
                     y='',
                     symbol_size=20,
                     line_width=1,
                     repulsion=500,
                     is_draggable=True,
                     width="800px",
                     height="500px",
                     path='timelineExample.html',
                     title='Timeline_graph',
                     subtitle='',
                     pageLayout=Page.DraggablePageLayout,
                     layout="circular",
                     show_node_value=True,
                     render=True):
    """
        A method to render a network with timeline.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            An object which represents a temporal, directed graph consisting of nodes and temporal arcs.
        h : int
            The threshold of temporal reachability. Nodes will be assigned different color based on this value.
        x : String
            The name of the x coordinates of the nodes.
            For example, in the network of London subway stations, the name of x coordinate can be 'lon' or 'lat'.
        y : String
            The name of the y coordinates of the nodes.
            For example, in the network of London subway stations, the name of x coordinate can be 'lon' or 'lat'.
        symbol_size : int
            The size of the nodes.
        line_width : int
            The width of the edges.
        repulsion : int
            The repulsion between nodes.
        is_draggable : boolean
            Whether the nodes are moveable.
        width: String
            The width of the image.
            Default value: 800px
        height: String
            The height of the image.
            Decault value: 500px
        path : String
            The path of the rendered image.
            Default value: circleExample.html
        title : String
            The title of the rendered image.
            Default value: Circle_Graph
        subtitle : String
            The subtitle of the rendered image.
            Default value: ''
        pageLayout : PageLayoutOpts
            There are two kinds of page layout: Page.DraggablePageLayout and Page.SimplePageLayout.
            In Page.SimplePageLayout, the width and height of the image border is stable.
            While in Page.DraggablePageLayout, the image border can be changed.
            Default value: Page.DraggablePageLayout
        layout : String
            There are three kinds of image layout: circular, force and none
            If the layout is none, you have to provide the x-coordinate and y-coordinate of nodes.
        show_node_value : boolean
            Whether show the reachability of nodes.
            Default value: True
        render : boolean
            Whether generate the html file directly.
            Default value: True

        Returns:
        --------
        c : Graph
            basic charts object in pyecharts package
    """

    # initialize nodes list
    nodes = []
    if layout == 'none':
        for i in range(len(graph.nodes.aslist())):
            # calculate reachability for each nodes
            reachability = ot.calculate_reachability(graph, graph.nodes.labels()[i])
            if reachability > h:
                # nodes with reachability more than h will be assigned category 0
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            x=graph.nodes.aslist()[i].data[x],
                                            y=graph.nodes.aslist()[i].data[y],
                                            category=0,
                                            value=reachability))
            else:
                # nodes with reachability less than or equal to h will be assigned category 1
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            x=graph.nodes.aslist()[i].data[x],
                                            y=graph.nodes.aslist()[i].data[y],
                                            category=1,
                                            value=reachability))
    else:
        for i in range(len(graph.nodes.aslist())):
            # calculate reachability for each nodes
            reachability = ot.calculate_reachability(graph, graph.nodes.labels()[i])
            if reachability > h:
                # nodes with reachability more than h will be assigned category 0
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=0,
                                            value=reachability))
            else:
                # nodes with reachability less than or equal to h will be assigned category 1
                nodes.append(opts.GraphNode(name=graph.nodes.labels()[i],
                                            category=1,
                                            value=reachability))

    # initialize links list
    links = []
    for i in graph.edges.timespan():
        tmpLinks = []
        for j in range(len(graph.edges.labels())):

            if graph.edges.start_times()[j] == i:
                tmp = graph.edges.labels()[j].split('-')
                edgeval = '{start time: ' + str(graph.edges.start_times()[j]) + ', end time: ' + str(
                    graph.edges.end_times()[j]) + '}'
                tmpLinks.append(opts.GraphLink(source=tmp[0], target=tmp[1], value=edgeval))
        links.append(tmpLinks)

    # initialize categories list
    categories = [
        opts.GraphCategory(name='nodes with reachability more than {}'.format(h)),
        opts.GraphCategory(name='nodes with reachability less than or equal to {}'.format(h))
    ]

    tl = Timeline()
    for i in graph.edges.timespan():
        c = (
            Graph(init_opts=opts.InitOpts(width=width, height=height))
                .add(
                "",
                nodes=nodes,
                links=links[i - graph.edges.start_times()[0]],
                categories=categories,
                layout=layout,
                is_draggable=is_draggable,
                is_rotate_label=True,
                symbol_size=symbol_size,
                linestyle_opts=opts.LineStyleOpts(is_show=True, curve=0.1, color="source", width=line_width),
                label_opts=opts.LabelOpts(position="right"),
                edge_symbol=['circle', 'arrow'],
                edge_symbol_size=10
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title=title, subtitle=subtitle,
                                          title_textstyle_opts=opts.TextStyleOpts(font_size=40),
                                          subtitle_textstyle_opts=opts.TextStyleOpts(font_size=20)),
                legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%",
                                            textstyle_opts=opts.TextStyleOpts(font_size=20)),
            )
        )
        tl.add(c, "{}".format(i))

    # if render is True, generate an html file
    if render:
        page = Page(layout=pageLayout)
        page.add(tl)
        page.render(path)

    return c


def ShowDifference(graph, algorithm, h, width='1200px', height='600px', x='', y='', layout='circular',
                   path='showDifference.html', pageLayout=Page.DraggablePageLayout, show_edge_value=True):
    """
        A method to generate a html file that contains network before and after running the h/c-approximation algorithm,
        and return a set of edges E_ such that (G,λ)\E_ has temporal reachability at most h.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            An object which represents a temporal, directed graph consisting of nodes and temporal arcs.
        algorithm : String
            'c' : run the c-approximation algorithm
            'h' : run the h-approximation algorithm
        h : int
            The threshold of temporal reachability. Nodes will be assigned different color based on this value.
        width: String
            The width of the image.
            Default value: 1200px
        height: String
            The height of the image.
            Decault value: 600px
        x : String
            The name of the x coordinates of the nodes.
            For example, in the network of London subway stations, the name of x coordinate can be 'lon' or 'lat'.
        y : String
            The name of the y coordinates of the nodes.
            For example, in the network of London subway stations, the name of x coordinate can be 'lon' or 'lat'.
        layout : String
            There are three kinds of image layout: circular, force and none
            If the layout is none, you have to provide the x-coordinate and y-coordinate of nodes.
        path : String
            The path of the rendered image.
            Default value: circleExample.html
        pageLayout : PageLayoutOpts
            There are two kinds of page layout: Page.DraggablePageLayout and Page.SimplePageLayout.
            In Page.SimplePageLayout, the width and height of the image border is stable.
            While in Page.DraggablePageLayout, the image border can be changed.
            Default value: Page.DraggablePageLayout
        show_edge_value : boolean
            Whether show the start time and end time of edges.
            Default value: True

        Returns:
        --------
        E_ : list
            a set of edges such that (G,λ)/E_ has temporal reachability at most h.
    """

    # target edge list
    E_ = []

    # copy the network
    tmpGraph = copy.deepcopy(graph)
    if algorithm == 'h':
        E_ = edgeDeletion.h_approximation(tmpGraph, h)
    elif algorithm == 'c':
        E_ = edgeDeletion.c_approximation(tmpGraph, h)

    if layout == 'circular':
        print('-----processing network one -----')
        c1 = echarts_Circular(graph,
                              h,
                              width=width,
                              height=height,
                              show_edge_value=show_edge_value,
                              title='network before running {}-approximation algorithm'.format(algorithm),
                              render=False)
        print('-----finished processing-----')

        print('-----processing network two-----')
        c2 = echarts_Circular(tmpGraph,
                              h,
                              width=width,
                              height=height,
                              show_edge_value=show_edge_value,
                              title='network after running {}-approximation algorithm'.format(algorithm),
                              render=False)
        print('-----finished processing-----')


    elif layout == 'force':
        print('-----processing network one -----')
        c1 = echarts_Force(graph,
                           h,
                           width=width,
                           height=height,
                           is_draggable=False,
                           show_edge_value=show_edge_value,
                           title='network before running {}-approximation algorithm'.format(algorithm),
                           render=False)
        print('-----finished processing-----')

        print('-----processing network two-----')
        c2 = echarts_Force(tmpGraph,
                           h,
                           width=width,
                           height=height,
                           is_draggable=False,
                           show_edge_value=show_edge_value,
                           title='network after running {}-approximation algorithm'.format(algorithm),
                           render=False)
        print('-----finished processing-----')


    elif layout == 'location':
        print('-----processing network one -----')
        c1 = echarts_Location(graph,
                              h,
                              x,
                              y,
                              width="1400px",
                              height="800px",
                              show_edge_value=show_edge_value,
                              title='network before running {}-approximation algorithm'.format(algorithm),
                              render=False)
        print('-----finished processing-----')

        print('-----processing network two-----')
        c2 = echarts_Location(tmpGraph,
                              h,
                              x,
                              y,
                              width="1400px",
                              height="800px",
                              show_edge_value=show_edge_value,
                              title='network after running {}-approximation algorithm'.format(algorithm),
                              render=False)
        print('-----finished processing-----')

    page = Page(layout=pageLayout)
    page.add(c1, c2)
    page.render(path)

    return E_