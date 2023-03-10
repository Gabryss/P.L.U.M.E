from graph import Graph
from display import Display
from algorithm import Algorithm
from tools import Color
import sys

GRID_SIZE = 3
DEFAULT_PATH = "data/images/graph_0"


def generation_logic(graph):
    """
    Main logic of the graph generation
    """

    # Starting point
    starting_point = graph.grid_size // 2
    graph.add_node(1, coordinates_p=[0.0,0.0], grid_coordinates_p=[starting_point, starting_point], active_p=True)

    # Main logic
    algorithm = Algorithm()
    algorithm.probabilistic(graph, 10)

    # Save the graph
    graph.save_grid()


def main(argv):
    # Check parameters  
    if len(argv) == 1 or len(argv) > 2:
        print(f"{Color.WARNING.value}Wrong number of arguments provided.\nDefault grid size selected{Color.ENDC.value}\n\n")
        grid_size = GRID_SIZE

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
    # grap.create_random_graph(25)


    # Display graph
    print(f"\n{Color.OKBLUE.value}End of generation.. Exporting the graph{Color.ENDC.value}")
    display = Display()
    display.process_graph(graph)
    display.create_figure()
    display.save_as(DEFAULT_PATH,"png")


if __name__ == '__main__':
    main(sys.argv)
