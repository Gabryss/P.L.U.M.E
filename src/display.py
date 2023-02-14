"""
Display a graph using Plotly library
"""

import plotly.graph_objs as go


class display():

    def __init__(self, node_width_p = 15, edge_width_p = 2, node_color_p = "red", edge_color_p = "blue"):
        self.figure = go.Figure()
        self.nodes = []
        self.edges = []
        self.nodes_color = node_color_p
        self.edges_color = edge_color_p
        self.nodes_size = node_width_p
        self.edges_width = edge_width_p
    

    def save_as(self, path_p="graphs/graph1", format_p="png"):
        """
        Path is without the format.
        Save the graph in the desired format
        Available formats:
            -png
            -jpeg
            -webp
            -svg
            -json
        """
        full_name = path_p + format_p
        self.figure.write_image(full_name, engine="kaleido")


    def process_graph(self, graph_p):
        """
        Take in input the nodes and edges of the graph and store the important parameters for the
        rendering inside the display class.
        """
        self.nodes = graph_p.nodes
        self.edges = self.remove_dupliacte_tuples(graph_p.get_edges())


    def create_figure(self):
        """
        Render the graph in the figure object
        """

        # Create a scatter plot for each node
        for node in self.nodes:
            self.figure.add_trace(go.Scatter(
                x=[node.coordinates['x']],
                y=[node.coordinates['y']],
                text=[node.id],
                mode='markers',
                marker=dict(size=self.nodes_size, color=self.nodes_color)
            ))

        # Create a line plot for each edge
        for edge in self.edges:
            self.figure.add_shape(
                type='line',
                x0=self.nodes[edge[0]].coordinates['x'],
                y0=self.nodes[edge[0]].coordinates['y'],
                x1=self.nodes[edge[1]].coordinates['x'],
                y1=self.nodes[edge[1]].coordinates['y'],
                line=dict(width=self.edges_width, color=self.edges_color)
            )


    def remove_dupliacte_tuples(self,tuple_list_p):
        """
        Takes a list of tuple in parameter and return a list of unique tuples irrespective of 
        their order.
        """
        unique_tuples = []

        for t in tuple_list_p:
            if sorted(t) not in [sorted(x) for x in unique_tuples]:
                unique_tuples.append(t)

        return unique_tuples





# nodes = [{'id': 0, 'x': 0, 'y': 0},
#          {'id': 1, 'x': 1, 'y': 0},
#          {'id': 2, 'x': 1, 'y': 2},
#          {'id': 3, 'x': 3, 'y': 3}]

# edges = [(0, 1), (0, 2), (1, 3)]