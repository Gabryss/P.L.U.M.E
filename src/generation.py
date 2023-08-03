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

    def __init__(self, nb_graphs_p, name_p) -> None:       
        # Get the number of graphs
        if nb_graphs_p == None or '':
            self.nb_graphs = Config.DEFAULT_NB_GRAPHS.value
        else:
            self.nb_graphs = nb_graphs_p
        
        # Get the name of the current graph generation
        if name_p == None or '':
            self.name = Config.DEFAULT_NAME.value
        else:
            self.name = name_p +"_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        

        self.graphs=[]
        # Make n graphs in different CPU cores
        list_process = [i for i in range(self.nb_graphs)]
        with multiprocessing.Pool(processes=self.nb_graphs) as pool:
            result = pool.map(self.generator, list_process)


    def generator(self, index_p):
        """
        Main generation frame. Used for multiprocessing
        """
        index = index_p
        current_graph = self.generate_graph(index)
        
        # Create picture for n graphs
        if Config.SAVE_GRAPH_IMAGE.value:
                self.create_graph_picture(current_graph, index)

        # Create the mesh
        if Config.DEFAULT_MESH_GENERATION.value:
                self.create_mesh(index)


    def generate_graph(self, index_p):
        """
        Main logic of the graph generation
        """
        
        print(f"{Color.OKBLUE.value} == Graph generation begins == {Color.ENDC.value}\n")
        
        # Graph generation
        index = index_p
        graph = Graph(self.name, index, Config.MAX_CREATED_NODE_ON_CIRCLE.value)

        # Starting point
        graph.add_node(node_id_p=0, coordinates_p=[0.0,0.0], radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value), active_p=True)

        # Main logic
        algorithm = Algorithm(graph_p=graph, min_nodes_p=Config.DEFAULT_MIN_NODES.value, loop_closure_probability_p=Config.DEFAULT_LOOP_CLOSURE_PROBABILITY.value)
        algorithm.algorithm(Config.SELECTED_ALGORITHM.value)

        # Save the graph
        graph.save_graph()
        print(f"\n{Color.OKBLUE.value} == End of graph generation == {Color.ENDC.value}")
        return graph


    def create_graph_picture(self, graph_p, index_p):
        """
        Display the created graph
        """
        graph = graph_p
        index = index_p
        print(f"\n{Color.OKBLUE.value} == Exporting the graph == {Color.ENDC.value}")
        display = Display(nb_graphs_p=index, generation_name_p=self.name)
        display.process_graph(graph)
        display.create_figure()
        display.create_image_from_graph()
        graph.create_adjency_matrix(graph.num_nodes)
        print(graph.adj_matrix)
        print(f"\n{Color.OKBLUE.value} == End of exportation == {Color.ENDC.value}")


    def create_mesh(self, index_p):
        """
        Create the mesh using Blender
        """
        index = index_p
        print(f"\n{Color.OKBLUE.value}Mesh generation start{Color.ENDC.value}")
        result = None
        blender_path = Tools.find_file("blender")
        try:
            if Config.DEFAULT_GUI_DISPLAY.value:
                result = subprocess.run(f"{blender_path} --python src/blender.py -index {index} -name {self.name}", shell=True, check=True)
            else:
                result = subprocess.run(f"{blender_path} --background --python src/blender.py -index {index} -name {self.name}", shell=True, check=True)
        
        except Exception as e:
            print(f"\n{Color.FAIL.value}An issue occured: ",e)
            print(f"The blender path might be wrong: ", Config.DEFAULT_BLENDER_PATH.value)
            print(f"If it is the case, please remove the path.json file{Color.ENDC.value}")

        finally:
            if result:
                success = result.stdout
                if success:
                    print("Success: ", success)
                
                error = result.stderr
                if error:
                    print("Error: ", error)
            print(f"\n{Color.OKBLUE.value}Mesh generation finished{Color.ENDC.value}")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                description="PLUME project. Procedural Lava-Tube Underground Modeling Engine: A generator that uses procedural generation techniques and graph algorithms to create detailed and visually appealing lava tube structures. ",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-nb_g", help="Number of graphs to generate", type=int)
    parser.add_argument("-name", help="Name of the current graph generation", type=str)

    args = parser.parse_args()
    arguments = vars(args)
    generator = Generator(nb_graphs_p=arguments['nb_g'],
                          name_p=arguments['name'])