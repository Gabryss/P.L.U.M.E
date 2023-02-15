from graph import Graph
from display import Display
from algorithm import Algorithm
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
        print("Wrong number of arguments provided.\nDefault grid size selected\n\n")
        grid_size = GRID_SIZE

    else:
        try:
            argv[1] = int(argv[1])
        except:
            return print("Please provide an integer")

        grid_size = argv[1]


    # Graph generation
    print("Generation begins")
    graph = Graph(grid_size)

    # Create the graph with the implemented logic
    generation_logic(graph)
    # grap.create_random_graph(25)


    # Display graph
    print("End of generation.. Exporting the graph")
    display = Display()
    display.process_graph(graph)
    display.create_figure()
    display.save_as(DEFAULT_PATH,"png")


if __name__ == '__main__':
    main(sys.argv)
