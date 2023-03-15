"""
Display a graph using Plotly library
"""

import plotly.graph_objs as go
import os
from tools import Color

DUMB = True

class Display():

    def __init__(self, node_width_p = 15, edge_width_p = 2, node_color_p = "red", edge_color_p = "blue"):
        
        self.figure = go.Figure()
        self.figure.update_layout(paper_bgcolor = 'darkgrey')
        
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
    

    def save_as(self, path_p="data/images/grap_h0", format_p="png"):
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
        full_path = path_p + "." + format_p

        if os.path.exists(full_path) and DUMB == False:
            print(f"\n{Color.WARNING.value}This path already exist\nGenerate auto path{Color.ENDC.value}")
            i = 0
            path="data/images/graph_"
            full_path = path+str(i)+"."+format_p
            while os.path.exists(full_path):
                i+=1
                full_path = path+str(i)+"."+format_p
            self.figure.write_image(full_path, engine="kaleido")
            

        else:
            self.figure.write_image(full_path, engine="kaleido")

        print(f"{Color.BOLD.value}Graph exported at", full_path,f"{Color.ENDC.value}")


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