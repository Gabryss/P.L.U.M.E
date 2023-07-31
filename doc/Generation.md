This Python script contains a Generator class for graph generation and visualizations. The graphs are procedurally generated and visualized using mesh models.

## Prerequisites

- Python
- graph module (local)
- display module (local)
- algorithm module (local)
- config module (local)
- subprocess module
- argparse module
- datetime module
- multiprocessing module
- tools module (local)

## Imports

- `Graph`: Local module for handling graph generation.
- `Display`: Local module for handling display of generated graphs.
- `Algorithm`: Local module for the main logic of graph generation.
- `Config` and `Color`: Local modules for application-wide configurations and color codes.
- `subprocess`: Python module for creating new processes.
- `argparse`: Python module for writing user-friendly command-line interfaces.
- `datetime`: Python module for manipulating dates and times.
- `multiprocessing`: Python module for using multiple processors for parallel execution.
- `tools`: Local module containing various utility functions.

## Class `Generator`

This class initializes the graph generation process and manages the process of generating multiple graphs, each in a separate CPU core.

- **Constructor (`__init__`):** Initializes the `Generator` instance with a specified grid size, number of graphs to generate, and the name of the graph generation. If no values are provided, defaults are used from the `Config` class. Multiple graph generation processes are started in parallel using the `multiprocessing` module.
    
- **`generator` method:** This method orchestrates the process of generating a graph, creating a visual representation of the graph, and creating a mesh if enabled in the `Config`. The whole generation is completed with: 1) Generation of the graph, 2) If needed an image representation and then 3) Mesh generation using Blender based on the generated coordinates and link of the graph.
    
- **`generate_graph` method:** This method manages the main logic of the graph generation. It creates a `Graph` object, selects a starting point, and applies the algorithm for graph generation.
    
- **`create_graph_picture` method:** This method visualizes the created graph.
    
- **`create_mesh` method:** This method initiates the creation of a mesh using the Blender software. It launches a subprocess to run Blender with a Python script and handle any exceptions that occur.
    

The script also contains a main function that takes command-line arguments for the initial grid size, the number of graphs to generate, and the name of the current graph generation. It then initializes a `Generator` instance with the provided arguments.

## Execution

This script can be run directly from the command-line with optional arguments for grid size, number of graphs, and the generation name. It uses these parameters to generate the desired number of graphs and visualize them.