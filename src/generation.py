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

class Generator:

    def __init__(self, name_p) -> None:       
        # Get the number of graphs
        self.nb_graphs = Config.NB_GENERATION.value
        self.visualization = Config.OPEN_VISUALIZATION.value
        self.graphs=[]

        # Get the name of the current graph generation
        if name_p == None or '':
            self.name = Config.DEFAULT_NAME.value
        else:
            self.name = name_p +"_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        # Start generation
        if self.nb_graphs==1:
            self.generator(0)
            # Create the mesh
            if Config.GENERATE_MESH.value:
                self.create_mesh(0)
        
        elif Config.PARALLELIZATION.value:
            # Make n graphs in different CPU cores (Only for the graph generation)  
            if self.nb_graphs>1:
                list_process = [i for i in range(self.nb_graphs)]
                with multiprocessing.Pool(processes=self.nb_graphs) as pool:
                    result = pool.map(self.generator, list_process)
                # Create the mesh
                if Config.GENERATE_MESH.value:
                    for index in list_process:
                        self.create_mesh(index)

            else:
                print(f"{Color.FAIL.value}Number of graphs not valid{Color.ENDC.value}")
                exit()
        
        else:
            if self.nb_graphs>1:
                for index in range(self.nb_graphs):
                    self.generator(index)
                    if Config.GENERATE_MESH.value:
                        self.create_mesh(index)
            else:
                print(f"{Color.FAIL.value}Number of graphs not valid{Color.ENDC.value}")
                exit()



    def generator(self, index_p):
        """
        Main generation frame. Used for multiprocessing
        """
        index = index_p
        current_graph = self.generate_graph(index)
        
        # Create picture for n graphs
        if Config.SAVE_GRAPH_IMAGE.value:
                self.create_graph_picture(current_graph, index)


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
        graph.add_node(node_id_p=0, coordinates_p=[0.0,0.0], radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value), active_p=True)
        print("\t-First node added")

        # Main logic
        algorithm = Algorithm(graph_p=graph, min_nodes_p=Config.DEFAULT_MIN_NODES.value, loop_closure_probability_p=Config.DEFAULT_LOOP_CLOSURE_PROBABILITY.value)
        algorithm.algorithm(Config.SELECTED_ALGORITHM.value)
        print("\t-Algorithm applied to the graph")

        processed_graph = self.post_processing_graph(graph_p=graph)
        print("\t-Post processing algorithm applied to the graph")

        graph.create_adjency_matrix(graph.nb_nodes)
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
    

    def create_graph_picture(self, graph_p, index_p):
        """
        Display the created graph
        """
        graph = graph_p
        index = index_p
        print(f"\n{Color.OKBLUE.value} == Graph {index} picture generation == {Color.ENDC.value}")
        display = Display(nb_graphs_p=index, generation_name_p=self.name)
        print("\t-Display object created")
        display.process_graph(graph)
        print("\t-Graph important features imported")
        display.create_figure()
        print("\t-Image created")
        display.create_image_from_graph()
        print("\t-Image saved")        
        print(f"{Color.OKBLUE.value} == End of graph {index} picture generation == {Color.ENDC.value}")


    def create_mesh(self, index_p):
        """
        Create the mesh using Blender
        """
        index = index_p
        print(f"\n{Color.OKBLUE.value} == Mesh {index} generation start == {Color.ENDC.value}")
        result = None
        blender_path = Tools.find_file("blender")
        try:
            if Config.OPEN_VISUALIZATION.value and index == self.nb_graphs-1:
                result = subprocess.run(f"{blender_path} --python src/blender.py -- -index {index} -name {self.name}", shell=True, check=True)
            else:
                result = subprocess.run(f"{blender_path} --background --python src/blender.py -- -index {index} -name {self.name}", shell=True, check=True)
        
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
            print(f"\n{Color.OKBLUE.value} == Mesh {index} generation finished == {Color.ENDC.value}")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                description="PLUME project. Procedural Lava-Tube Underground Modeling Engine: A generator that uses procedural generation techniques and graph algorithms to create detailed and visually appealing lava tube structures. ",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-name", help="Name of the current graph generation", type=str)

    args = parser.parse_args()
    arguments = vars(args)
    generator = Generator(name_p=arguments['name'])