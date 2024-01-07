"""
Display a graph using Plotly library
"""

# import plotly.graph_objs as go
import plotly
import plotly.graph_objects as go
import plotly.express as px
import os
from config import Config, Color
import pandas as pd
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
        import matplotlib.pyplot as plt
        if self._3dimension :
            # x = np.array(range(-20, 20, 0.1))
            # y = np.array(range(-20, 20, 0.1))
            # z = np.array(range(-20, 20, 0.1))
            # Xgrid, Ygrid, Zgrid = np.meshgrid(x,y,z)
            Xgrid, Ygrid, Zgrid = np.mgrid[-10:10:50j, -10:10:50j, -10:10:50j]

            # fig = plt.figure()
            # ax = fig.add_subplot(projection='3d')
            # for node in self.nodes:
            #     cX, cY, cZ = self.nodes[node].coordinates['x'],self.nodes[node].coordinates['y'],self.nodes[node].coordinates['z']
            #     radius = self.nodes[node].radius
                
            #     check = (Xgrid - cX)**2 + (Ygrid - cY)**2 + (Zgrid - cZ)**2 <= radius**2
            #     # print(check, check.shape)
            #     # print(Xgrid[check], Xgrid[check].shape)
                
            #     # array = np.r_[array,[[self.nodes[node].coordinates['x'],self.nodes[node].coordinates['y'],self.nodes[node].coordinates['z']]]]
            #     ax.scatter(Xgrid[check], Ygrid[check], Zgrid[check], color='green')

            # ax.set_title('сетка из точек 100х100',
            #             fontfamily = 'monospace',
            #             fontstyle = 'normal',
            #             fontweight = 'bold',
            #             fontsize = 10)
            # ax.set_xlabel("Value", fontsize=14)
            # ax.set_ylabel("Square of Value", fontsize=14)

            # ax.set_xlim3d(-50, 50)
            # ax.set_ylim3d(-50, 50)
            # ax.set_zlim3d(-50, 50)

            # plt.show()
            count = 0
            for node in self.nodes:
                count +=1
                if self.nodes[node].id == 0:
                    cX, cY, cZ = self.nodes[node].coordinates['x'],self.nodes[node].coordinates['y'],self.nodes[node].coordinates['z']
                    radius = 0.5
                    values = (Xgrid - cX)**2 + (Ygrid - cY)**2 + (Zgrid - cZ)**2 <= radius**2
                    # values=values.flatten()




                # test = plotly.graph_objects.Volume(
                #     x=Xgrid.flatten(),
                #     y=Ygrid.flatten(),
                #     z=Zgrid.flatten(),
                #     value=values.flatten(),
                #     isomin=-0.1,
                #     isomax=0.8,
                #     opacity=0.1, # needs to be small to see through all surfaces
                #     surface_count=25, # needs to be a large number for good volume rendering
                # )
                # data_3d.append(plotly.graph_objects.Volume(
                #     x=Xgrid.flatten(),
                #     y=Ygrid.flatten(),
                #     z=Zgrid.flatten(),
                #     value=values.flatten(),
                #     isomin=-0.1,
                #     isomax=0.8,
                #     opacity=0.1, # needs to be small to see through all surfaces
                #     surface_count=17, # needs to be a large number for good volume rendering
                # ))
                
                else:
                    cX, cY, cZ = self.nodes[node].coordinates['x'],self.nodes[node].coordinates['y'],self.nodes[node].coordinates['z']
                    radius = 0.5
                    new_values = (Xgrid - cX)**2 + (Ygrid - cY)**2 + (Zgrid - cZ)**2 <= radius**2
                    # new_values.flatten()

                    values = np.logical_or(values, new_values)
                    # for i in range(len(values)):
                    #     for j in range(len(values)):
                    #         for k in range(len(values)):
                    #             if new_values[i][j][k] == True:
                    #                 values[i][j][k] == True
                    
                    # print(values, values.shape)
                    # print(Xgrid[values], Xgrid[values].shape)
                
            
            self.figure.add_trace(go.Streamtube(x=[0, 0, 1], y=[0, 1, 2], z=[0, 0, 0], 
                                       u=[0, 0, 0], v=[1, 1, 1], w=[0, 0, 0]))

            # X, Y, Z = np.mgrid[-1:1:30j, -1:1:30j, -1:1:30j]            # values = np.sin(X*Y*Z) / (X*Y*Z)
            # values = np.sin(np.pi*X) * np.cos(np.pi*Z) * np.sin(np.pi*Y)
            # self.figure = go.Figure(data=data_3d)
            self.figure = go.Figure(data=go.Volume(
                x=Xgrid.flatten(),
                y=Ygrid.flatten(),
                z=Zgrid.flatten(),
                value=values.flatten(),
                isomin=-1,
                isomax=1,
                opacity=0.1, # needs to be small to see through all surfaces
                surface_count=20, # needs to be a large number for good volume rendering
                ))
            
            df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/streamtube-wind.csv').drop(['Unnamed: 0'],axis=1)
            print(df)
            print(df['x'])
            x, y, z = np.mgrid[0:10, 0:10, 0:10]
            x = x.flatten()
            y = y.flatten()
            z = z.flatten()

            u = np.zeros_like(x)
            v = np.zeros_like(y)
            w = z**2
            self.figure.add_trace(go.Streamtube(x=x,
                                                y=y,
                                                z=z,
                                                u=u,
                                                v=v,
                                                w=w))

            # self.figure = go.Figure(data=go.Isosurface(
            #     x=[0,0,0,0,2,2,2,2],
            #     y=[3,0,3,0,3,0,3,0],
            #     z=[2,2,5,5,2,2,5,5],
            #     value=[2,2,3,4,5,6,7,8],
            #     isomin=2,
            #     isomax=6,
            #     colorscale='magma',
            # ))

            
            self.figure.update_layout(template='plotly_dark', title=f"Generation {self.generation_name}")




            # self.figure.update_layout(scene_xaxis_showticklabels=False,
            #                 scene_yaxis_showticklabels=False,
            #                 scene_zaxis_showticklabels=False)

            # for edge in self.edges:
            #     # df = px.data.gapminder().query("continent=='Europe'")
            #     data = {'x':self.nodes[edge[0]].coordinates['x'], 'y':self.nodes[edge[0]].coordinates['y'],  'z':self.nodes[edge[0]].coordinates['z']}
            #     df1 = pd.DataFrame([data])
            #     df = pd.concat([df, df1], ignore_index=True)

            #     data = {'x':self.nodes[edge[1]].coordinates['x'], 'y':self.nodes[edge[1]].coordinates['y'],  'z':self.nodes[edge[1]].coordinates['z']}
            #     df1 = pd.DataFrame([data])
            #     df = pd.concat([df, df1], ignore_index=True)
            # print(df)


                
            # self.figure = px.line_3d(df, x="x", y="y", z="z")
            # self.figure.show()

            # df = px.data.iris()
            
            
            #Scatter
            # self.figure = px.scatter_3d(df, x='x', y='y', z='z',
            #             size_max=18,
            #             opacity=0.7)
            

            # # tight layout
            # self.figure.update_layout(margin=dict(l=0, r=0, b=0, t=0))
            self.figure.show()

        else:
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
            self.figure.update_layout(template='plotly_dark', title=f"Generation {self.generation_name}")
            self.figure.show()

