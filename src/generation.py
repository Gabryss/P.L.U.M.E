from graph import Graph
from display import Display
from algorithm import Algorithm
from config import Color, Config
import subprocess
import argparse
import datetime
import multiprocessing

class Generator:

    def __init__(self, grid_size_p, nb_graphs_p, name_p) -> None:
        # Get the grid size
        if grid_size_p == None or '':
            self.grid_size = Config.INITIAL_GRID_SIZE.value
        else:
            self.grid_size = grid_size_p
        
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
        # Make n graphs
        list_process = [i for i in range(self.nb_graphs)]
        with multiprocessing.Pool(processes=self.nb_graphs) as pool:
            result = pool.map(self.generator, list_process)
        
        # for index in range(self.nb_graphs):
        #     self.graphs.append(self.generate_graph(index))
        #     current_graph  = self.graphs[index]
            
        #     # Create picture for n graphs
        #     if Config.SAVE_GRAPH_IMAGE.value:
        #             self.create_graph_picture(current_graph, index)

        #     # Create the mesh
        #     if Config.DEFAULT_MESH_GENERATION.value:
        #             self.create_mesh(index)
    
    def generator(self, index_p):
        """
        Main generation frame. Used for multiprocessing
        """
        index = index_p
        # self.graphs.append(self.generate_graph(index))
        # current_graph  = self.graphs[index]
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
        graph = Graph(self.grid_size, self.name, index)

        # Starting point
        starting_point = graph.grid_size // 2
        graph.add_node(1, coordinates_p=[0.0,0.0], grid_coordinates_p=[starting_point, starting_point], active_p=True)

        # Main logic
        algorithm = Algorithm(Config.DEFAULT_MIN_NODES.value, Config.DEFAULT_LOOP_CLOSURE_PROBABILITY.value)
        algorithm.probabilistic(graph, Config.DEFAULT_NB_ITERATION.value)

        # Save the graph
        graph.save_grid()
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
        print(f"\n{Color.OKBLUE.value} == End of exportation == {Color.ENDC.value}")

    
    def create_mesh(self, index_p):
        """
        Create the mesh using Blender
        """
        index = index_p
        print(f"\n{Color.OKBLUE.value}Mesh generation start{Color.ENDC.value}")
        print("DEBUG", Config.DEFAULT_BLENDER_PATH.value)
        if Config.DEFAULT_GUI_DISPLAY.value:
            result = subprocess.run(f"{Config.DEFAULT_BLENDER_PATH.value} --python src/blender.py -index {index} -name {self.name}", shell=True, check=True)
        else:
            result = subprocess.run(f"{Config.DEFAULT_BLENDER_PATH.value} --background --python src/blender.py -index {index} -name {self.name}", shell=True, check=True)

        success = result.stdout
        if success:
            print("Success: ", success)
        
        error = result.stderr
        if error:
            print("Error: ", error)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                description="PLUME project. Procedural Lava-Tube Underground Modeling Engine: A generator that uses procedural generation techniques and graph algorithms to create detailed and visually appealing lava tube structures. ",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-s", help="Initial grid size", type=int)
    parser.add_argument("-nb_g", help="Number of graphs to generate", type=int)
    parser.add_argument("-name", help="Name of the current graph generation", type=str)

    args = parser.parse_args()
    arguments = vars(args)
    generator = Generator(grid_size_p=arguments['s'],
                          nb_graphs_p=arguments['nb_g'],
                          name_p=arguments['name'])