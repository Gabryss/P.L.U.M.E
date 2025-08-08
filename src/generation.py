# SPDX-License-Identifier: BSD-3-Clause

from graph import Graph
from display import Display
from algorithm import Algorithm
from config import Color, Config
import subprocess
import argparse
import datetime
import multiprocessing
from tools import Tools
import random as rd
import time
import json
import os

class Generator:

    def __init__(self, name_p, graph_path_p) -> None:       
        # Get the number of graphs
        self.nb_graphs = Config.NB_GENERATION.value
        self.visualization = Config.OPEN_VISUALIZATION.value
        self.graphs=[]

        self.starting_time = time.time()
        self.graph_path = []

        # Get the name of the current graph generation
        if name_p == None or '':
            self.name = Config.DEFAULT_NAME.value
        else:
            self.name = name_p
        
        if graph_path_p == None or '':
            self.graph_path = None
        else:
            # Check if mutli-node generation
            self.name = f'{graph_path_p}_regen_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
            graph_path_p = f'{os.getcwd()}/data/{graph_path_p}'
            dir_ = os.listdir(graph_path_p)
            if os.path.isdir(f'{graph_path_p}/{dir_[0]}'):
                # Multi-node generation
                for path in dir_:
                    self.graph_path.append(str(f'{graph_path_p}/{path}'))
            else:
                self.graph_path = graph_path_p


        if self.graph_path:
            # Regenerate graph
            if type(self.graph_path) == list:
                index = 0
                for path in self.graph_path:
                    if Config.GENERATE_GRAPH_IMAGE.value:
                        saving_path = os.getcwd()+'/data/'+self.name+'/'+ str(index)
                        self.create_graph_picture(path_p=path, saving_path_p=saving_path)
                    self.create_mesh(index, graph_path_p=path)
                    index+=1
                                
            else:
                if Config.GENERATE_GRAPH_IMAGE.value:
                        saving_path = os.getcwd()+'/data/'+self.name
                        self.create_graph_picture(path_p=path, saving_path_p=saving_path)
                self.create_mesh(0, graph_path_p=self.graph_path)

        else:
            # Start generation
            if Config.PARALLELIZATION.value:
                # Make n graphs in different CPU cores (Only for the graph generation)  
                list_process = [i for i in range(self.nb_graphs)]
                with multiprocessing.Pool(processes=self.nb_graphs) as pool:
                    result = pool.map(self.generator, list_process)
                # Create the mesh
                if Config.GENERATE_MESH.value:
                    for index in list_process:
                        path = f'{os.getcwd()}/data/{self.name}/{index}'
                        self.create_mesh(index, graph_path_p=path)
            
            else:
                for index in range(self.nb_graphs):
                    path = os.getcwd()+'/data/'+self.name+'/'+str(index)
                    self.generator(index, path)
                    if Config.GENERATE_MESH.value:
                        duration = self.create_mesh(index, graph_path_p=path)
                        


    def generator(self, index_p, path_p):
        """
        Main generation frame. Used for multiprocessing
        """
        index = index_p
        self.generate_graph(index)
        
        # Create picture for n graphs
        if Config.GENERATE_GRAPH_IMAGE.value:
                self.create_graph_picture(path_p = path_p, saving_path_p=path_p)


    def generate_graph(self, index_p):
        """
        Main logic of the graph generation
        """
        index = index_p
        print(f"{Color.OKBLUE.value} == Graph {index} generation begins == {Color.ENDC.value}")
        
        
        # Graph generation
        index = index_p
        graph = Graph(self.name, index, Config.MAX_CREATED_NODE_ON_CIRCLE.value)
        print("\t-Graph created")

        # Starting point
        graph.add_node(node_id_p=0, coordinates_p=[0.0,0.0,0.0], radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value), active_p=True)
        print("\t-First node added")

        # Main logic
        algorithm = Algorithm(graph_p=graph, loop_closure_probability_p=Config.DEFAULT_LOOP_CLOSURE_PROBABILITY.value)
        algorithm.algorithm(Config.SELECTED_ALGORITHM.value)
        print("\t-Algorithm applied to the graph")

        processed_graph = self.post_processing_graph(graph_p=graph)
        print("\t-Post processing algorithm applied to the graph")

        processed_graph.create_adjency_matrix(graph.nb_nodes)
        print("\t-Adjency matrix created")

        # Save the graph
        processed_graph.save_graph()
        print("\t-Graph saved")

        # Display the adjency matrix
        print(f"{Color.BOLD.value}Adjency matrix:{Color.ENDC.value}")
        print(graph.adj_matrix)

        print(f"{Color.OKBLUE.value} == End of graph {index} generation == {Color.ENDC.value}")
        return processed_graph


    def post_processing_graph(self, graph_p):
        """
        Various post process solition applied to the graph. Currently:
        - Remove edge duplicates
        """
        # Remove duplicates
        graph = graph_p
        for node in graph.nodes:
            graph.nodes[node].set_edges(Tools.remove_duplicate_none_list(graph.nodes[node].get_edges()))
        
        return graph
    

    def create_graph_picture(self, path_p, saving_path_p):
        """
        Display the created graph
        """
        print(f"\n{Color.OKBLUE.value} == Graph picture generation == {Color.ENDC.value}")
        display = Display(data_path=path_p, voxel_size=0.6,
            node_radius=1.0,      # You can set per-node radii if desired
            edge_radius=1.0,      # You can set per-edge radii if desired
            smoothing=True,
            n_iter=50,
            relaxation_factor=0.1)
        print("\t-Display object created")
        display.load_graph()
        print("\t-Graph important features imported")
        display.voxelize()
        print("\t-Graph voxelized")
        display.extract_surface()
        print("\t-Graph surface extracted")
        
        if Config.ANIMATE.value:
            # Animate the graph
            print("\t-Starting graph animation")
            display.animate_bone_then_mesh_with_orbit(
                path=saving_path_p + "/cave_bone_then_mesh.mp4",
                tube_color="navy",
                mesh_opacity=1,
                n_skip_bone=1,    # Skip edges for faster bone growth animation
                n_skip_mesh=1,    # Skip for faster mesh growth (adjust as you want)
                orbit_frames=36,
                orbit_factor=1.3,)
            print("\t-Graph animated and saved as a video")

            
        if Config.GENERATE_GRAPH_IMAGE.value:
            # Create a static image of the graph
            display.create_static_image(saving_path_p + "/cave_graph.png", tube_color="navy", mesh_opacity=1)
            print("\t-Graph static image created")


        print("\t-Graph animated")
        if self.visualization:
            # Open the graph in a new window
            display.plot()
            print("\t-Graph displayed")
        # display.plot()
        print("\t-Graph plotted")     
        print(f"{Color.OKBLUE.value} == End of graph picture generation == {Color.ENDC.value}")


    def create_mesh(self, index_p, graph_path_p=None):
        """
        Create the mesh using Blender
        """
        blender_path = Tools.find_file("blender")
        index = index_p

        print(f"\n{Color.OKBLUE.value} == Mesh generation start == {Color.ENDC.value}")
        result = None
        try:
            if Config.DEBUG.value:
                result = subprocess.run(f"{blender_path} --python src/blender.py -- -g {graph_path_p} -index {index} -name {self.name}", shell=True, check=True)
            else:
                result = subprocess.run(f"{blender_path} --background --python src/blender.py -- -g {graph_path_p} -index {index} -name {self.name}", shell=True, check=True)
        
        except Exception as e:
            print(f"\n{Color.FAIL.value}An issue occured: ",e)
            print(f"The blender path might be wrong, please check the path.json file")
            print(f"If it is the case, please remove the path.json file{Color.ENDC.value}")
            exit()

        finally:
            if result:
                success = result.stdout
                if success:
                    print(f"{Color.OKGREEN.value}Success: ", success,f"{Color.ENDC.value}")
                
                error = result.stderr
                if error:
                    print(f"{Color.FAIL.value}Error: ", error,f"{Color.ENDC.value}")
            duration = (time.time() - self.starting_time) / 60
            print("Duration of the generation: ", duration," minutes")
            print(f"\n{Color.OKBLUE.value} == Mesh generation finished == {Color.ENDC.value}")
        
        return duration




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                description="PLUME project. Procedural Lava-Tube Underground Modeling Engine: A generator that uses procedural generation techniques and graph algorithms to create detailed and visually appealing lava tube structures. ",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-n", help="Name of the current graph generation", type=str)
    parser.add_argument("-g", help="Take an already generated graph as input", type=str)

    args = parser.parse_args()
    arguments = vars(args)
    generator = Generator(name_p=arguments['n'], graph_path_p=arguments['g'])