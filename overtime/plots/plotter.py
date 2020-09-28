
import math
import matplotlib.pyplot as plt
import imageio



class Plotter:
    """
        A class for creating various plots through pyplot.

        Object Propertie(s):
        --------------------
        plot : Plot
            The plot class to be used by the plotter.

        See also:
        ---------
            Plot
            Circle
            Slice
    """

    def __init__(self):
        self.plot = None


    def single(self, plot, graph, save=False, ordered=True, slider=True, show=True):
        """
            A method of Plotter.
            Parameter(s):
            -------------
            plot : Plot
                A valid Plot class/subclass.
            graph : Graph
                A valid Graph class/subclass.
            save : Boolean
                A switch to enable saving the figure to a file.
            ordered : Boolean
                If the Plot class supports the ordering of a plot in some useful way, enable it.
            slider : Boolean
                If the Plot class supports sliders, enable it.
            show : Boolean
                Show the plot (can be overridden).

            Returns:
            --------
            plot_object : Plot
                Also shows (and saves, if enabled) the resulting figure.
        """
        self.plot = plot # assign the plot class to the plotter.
        figure, axes = plt.subplots(1) # initialize the figure & axes.
        figure.set_size_inches(14, 10) # set the size of the figure window.
        # plot the graph.
        plot_object = self.plot(graph, figure, axes, ordered=ordered, slider=slider, show=show)
        # if save is enabled, save the figure.
        if save:
            self.save(figure, plot_object.name)
        # if the plot has not already been shown (through plt.show(), for example), show the figure.
        if show and plot_object.show:
            figure.show()
        return plot_object


    def singles(self, plot, graphs, save=False, ordered=True, slider=True, show=True):
        """
            A method of Plotter.
            Parameter(s):
            -------------
            plot : Plot
                A valid Plot class/subclass.
            graphs : List
                A valid list of Graph classes/subclasses.
            save : Boolean
                A switch to enable saving the figure to a file.
            ordered : Boolean
                If the Plot class supports the ordering of a plot in some useful way, enable it.
            slider : Boolean
                If the Plot class supports sliders, enable it.
            show : Boolean
                Show the plot (can be overridden).

            Returns:
            --------
            plot_objects : List
                Also shows (and saves, if enabled) the resulting figures.
        """
        # for each graph in the list supplied.
        plot_objects = []
        for graph in graphs:
            # plot each graph in it's respective figure.
            plot_objects.append(self.single(plot, graph, save=save, show=show))
        return plot_objects


    def gif(self, plot, graphs, ordered=True, file_name='graph'):
        """
            A method of Plotter.
            Parameter(s):
            -------------
            plot : Plot
                A valid Plot class/subclass.
            graphs : List
                A valid list of Graph classes/subclasses.
            ordered : Boolean
                If the Plot class supports the ordering of a plot in some useful way, enable it.
            file_name : String
                The name of the resulting gif file.

            Returns:
            --------
                None, saves each individual figure and creates a gif.
        """
        # plot and save each individual graph.
        plots = self.singles(plot, graphs, save=True, ordered=ordered, show=False)
        # gather the labels of the saved graph files.
        labels = [plot.name + '.png' for plot in plots]
        # read the images into imageio.
        images = [imageio.imread(f) for f in labels]
        # create and save the gif.
        imageio.mimsave(file_name + '/' + file_name + '.gif', images, duration=2)


    def multi(self, plot, graphs, save=False, ordered=True, file_name='multi', show=True):
        """
            A method of Plotter.
            Parameter(s):
            -------------
            plot : Plot
                A valid Plot class/subclass.
            graphs : List
                A valid list of Graph classes/subclasses.
            save : Boolean
                A switch to enable saving the figure to a file.
            ordered : Boolean
                If the Plot class supports the ordering of a plot in some useful way, enable it.
            file_name : String
                Added to file name if saved.
            show : Boolean
                Show the plot (can be overridden).

            Returns:
            --------
                None, saves each individual figure and creates a gif.
        """
        self.plot = plot # assign the plot class to the plotter.
        ncols = math.ceil(math.sqrt(len(graphs))) # number of subplot columns.
        nrows = math.ceil(len(graphs)/ncols) # number of subplot rows.
        figure, axes = plt.subplots(nrows, ncols) # initialize the figure & axes.
        figure.set_size_inches(14, 10) # set the size of the figure window.
        i = 0
        flag = False # flag if all plots are plotted.
        for row in axes:
            # if there is only one row in the figure, plot along it.
            if nrows == 1:
                self.plot(graphs[i], figure, row, ordered=ordered, show=show)
                i += 1
                # if last graph is processed, break.
                if i == len(graphs):
                    flag = True
                    break
            else:
                # for every column in the row.
                for col in row:
                    self.plot(graphs[i], figure, col, ordered=ordered, show=show)
                    i += 1
                    # if last graph is processed, break.
                    if i == len(graphs):
                        flag = True
                        break
            # if last graph has been flagged, break.
            if flag:
                break
        # number of remaining, unused axes.
        extra_axes = nrows * ncols - len(graphs)
        # for each unused axis.
        for x in range(ncols-extra_axes, ncols):
            figure.delaxes(axes[nrows-1][x]) # delete it.
        plt.tight_layout(pad=4) # apply a tight layout scheme.
        # if save is enabled, save the figure.
        if save:
            self.save(figure, plot.name)
        # if the plot has not already been shown (through plt.show(), for example), show the figure.
        if show:
            figure.show()


    def save(self, figure, label):
        """
            A method of Plotter.
            Parameter(s):
            -------------
            figure : Figure
                A pyplot figure object.
            label : String
                The name of the file to be saved.

            Returns:
            --------
                None, saves the figure to a file.
        """
        figure.savefig(label + '.png', format='png')
