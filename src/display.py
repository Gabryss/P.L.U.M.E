"""
Display a graph using Plotly library
"""

import plotly.graph_objects as go
import plotly.express as px
import os
from config import Config
from tqdm import tqdm
import numpy as np

class Display():

    def __init__(self, nb_graphs_p, generation_name_p, node_width_p = 15, edge_width_p = 2, node_color_p = "red", edge_color_p = "blue"):
        self.nb_graphs = f"/{str(nb_graphs_p)}"
        self.figure = go.Figure()
        self.generation_name = generation_name_p
        self._3dimension = Config.THREE_DIMENSION_GENERATION.value
        self.nodes = []
        self.edges = []
        self.nodes_color = node_color_p
        self.edges_color = edge_color_p
        self.nodes_size = node_width_p
        self.edges_width = edge_width_p
        self.save_image_path = Config.PLUME_DIR.value+"/data/"+self.generation_name+self.nb_graphs+"/graph"+Config.IMAGE_FORMAT.value
        self.save_html_image_path = Config.PLUME_DIR.value+"/data/"+self.generation_name+self.nb_graphs+"/graph.html"

    def save_image(self):
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

        if self._3dimension:
            self.figure.write_html(self.save_html_image_path)


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
        if self._3dimension :
   
            Xgrid, Ygrid, Zgrid = np.mgrid[-10:10:50j, -10:10:50j, -10:10:50j]
            count = 0
            for node in tqdm(self.nodes, desc="                Progress"):
                count +=1
                if self.nodes[node].id == 0:
                    cX, cY, cZ = self.nodes[node].coordinates['x'],self.nodes[node].coordinates['y'],self.nodes[node].coordinates['z']
                    radius = 0.5
                    values = (Xgrid - cX)**2 + (Ygrid - cY)**2 + (Zgrid - cZ)**2 <= radius**2
                
                else:
                    cX, cY, cZ = self.nodes[node].coordinates['x'], self.nodes[node].coordinates['y'], self.nodes[node].coordinates['z']
                    
                    radius = 0.5
                    new_values = (Xgrid - cX)**2 + (Ygrid - cY)**2 + (Zgrid - cZ)**2 <= radius**2
                    if count != len(self.nodes):
                        cX_next, cY_next, cZ_next = self.nodes[count].coordinates['x'], self.nodes[count].coordinates['y'], self.nodes[count].coordinates['z']
                        
                        c = np.array([cX, cY, cZ])
                        c_next = np.array([cX_next, cY_next, cZ_next])
                        dist = np.linalg.norm(c - c_next)

                        if dist <= 0.5:
                            x_f = np.linspace(c[0],c_next[0],1)
                            y_f = np.linspace(c[1],c_next[1],1)
                            z_f = np.linspace(c[2],c_next[2],1)
                        
                        else:
                            x_f = np.linspace(c[0],c_next[0],int(dist*1.5))
                            y_f = np.linspace(c[1],c_next[1],int(dist*1.5))
                            z_f = np.linspace(c[2],c_next[2],int(dist*1.5))
                        
                        for i in range(len(x_f)):
                            new_values+= (Xgrid - x_f[i])**2 + (Ygrid - y_f[i])**2 + (Zgrid - z_f[i])**2 <= radius**2

                    values = np.logical_or(values, new_values)


            self.figure = go.Figure(data=go.Volume(
                x=Xgrid.flatten(),
                y=Ygrid.flatten(),
                z=Zgrid.flatten(),
                value=values.flatten(),
                isomin=-1,
                isomax=1,
                opacity=0.2, # needs to be small to see through all surfaces
                surface_count=20, # needs to be a large number for good volume rendering
                caps= dict(x_show=True, y_show=True, z_show=True, x_fill=1),
                ))
            
            self.figure.update_layout(scene_xaxis_showticklabels=False,
                  scene_yaxis_showticklabels=False,
                  scene_zaxis_showticklabels=False)
            
            
            self.figure.update_layout(template='plotly_dark', title=f"Generation {self.generation_name}")

        else:
            # Create a scatter plot for each node
            for node in tqdm(self.nodes, desc="                Progress"):
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
            self.figure.update_layout(template='plotly_dark', title=f"Generation {self.generation_name}")

