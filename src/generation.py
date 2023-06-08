from graph import Graph
from display import Display
from algorithm import Algorithm
from tools import Color
import sys
import subprocess

DEFAULT_GRID_SIZE = 3
DEFAULT_NB_ITERATION = 100
DEFAULT_GRID_PATH = "data/images/graph_0"
DEFAULT_MIN_NODES = 15000
DEFAULT_LOOP_CLOSURE_PROBABILITY = 10
DEFAULT_GUI_DISPLAY = False
DEFAULT_GENERATE_PNG = False

def generation_logic(graph):
    """
    Main logic of the graph generation
    """

    # Starting point
    starting_point = graph.grid_size // 2
    graph.add_node(1, coordinates_p=[0.0,0.0], grid_coordinates_p=[starting_point, starting_point], active_p=True)

    # Main logic
    algorithm = Algorithm(DEFAULT_MIN_NODES, DEFAULT_LOOP_CLOSURE_PROBABILITY)
    algorithm.probabilistic(graph, DEFAULT_NB_ITERATION)

    # Save the graph
    graph.save_grid()
    graph.save_graph()


def main(argv):
    # Check parameters  
    if len(argv) == 1 or len(argv) > 2:
        print(f"{Color.WARNING.value}Wrong number of arguments provided.\nDefault grid size selected{Color.ENDC.value}\n\n")
        grid_size = DEFAULT_GRID_SIZE

    else:
        try:
            argv[1] = int(argv[1])
        except:
            return print(f"{Color.WARNING.value}Please provide an integer{Color.ENDC.value}")

        grid_size = argv[1]


    # Graph generation
    print(f"{Color.OKBLUE.value}Generation begins{Color.ENDC.value}\n")
    graph = Graph(grid_size)

    # Create the graph with the implemented logic
    generation_logic(graph)

    # Display graph
    if DEFAULT_GENERATE_PNG:
        print(f"\n{Color.OKBLUE.value}End of generation.. Exporting the graph{Color.ENDC.value}")
        display = Display()
        display.process_graph(graph)
        display.create_figure()
        display.save_as(DEFAULT_GRID_PATH,"png")

    print(f"\n{Color.OKBLUE.value}Mesh generation start{Color.ENDC.value}")
    if DEFAULT_GUI_DISPLAY:
        subprocess.run("/home/gabriel/Documents/blender-3.5.1-linux-x64/blender --python src/blender.py", shell=True, check=True)
    else:
        subprocess.run("/home/gabriel/Documents/blender-3.5.1-linux-x64/blender --background --python src/blender.py", shell=True, check=True)



if __name__ == '__main__':
    main(sys.argv)
