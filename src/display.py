"""
Display a graph using Plotly library
"""

import plotly.graph_objs as go
import os
from config import Config, Color



class Display():

    def __init__(self, nb_graphs_p, generation_name_p, node_width_p = 15, edge_width_p = 2, node_color_p = "red", edge_color_p = "blue"):
        self.nb_graphs = f"/{str(nb_graphs_p)}"
        self.figure = go.Figure()
        self.figure.update_layout(paper_bgcolor = 'darkgrey')
        self.generation_name = generation_name_p
        
        self.figure.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            tickfont=dict(family='Rockwell', color='black', size=14)
        )
        self.figure.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey',
            tickfont=dict(family='Rockwell', color='black', size=14)
        )
        self.nodes = []
        self.edges = []
        self.nodes_color = node_color_p
        self.edges_color = edge_color_p
        self.nodes_size = node_width_p
        self.edges_width = edge_width_p
        self.save_image_path = Config.PLUME_DIR.value+"/data/images/"+self.generation_name+self.nb_graphs+"/graph"+Config.IMAGE_FORMAT.value
    

    def create_image_from_graph(self):
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
        if not os.path.exists(os.path.dirname(self.save_image_path)):
            os.makedirs(os.path.dirname(self.save_image_path))
    
        self.figure.write_image(self.save_image_path, engine="kaleido")


    def process_graph(self, graph_p):
        """
        Take in input the nodes and edges of the graph and store the important parameters for the
        rendering inside the display class.
        """
        self.nodes = graph_p.nodes
        self.edges = graph_p.get_edges()


    def create_figure(self):
        """
        Render the graph in the figure object
        """
        # Create a scatter plot for each node
        for node in self.nodes:
            self.figure.add_trace(go.Scatter(
                x=[self.nodes[node].coordinates['x']],
                y=[self.nodes[node].coordinates['y']],
                text=[self.nodes[node].id],
                mode='markers+text',
                textposition="bottom center"
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
        
        self.figure.update_traces(textposition='top center')