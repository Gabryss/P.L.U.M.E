## Prerequisites

- Python
- Plotly

## Imports

- `plotly.graph_objs`: Plotly's graph objects module for creating figures and traces.
- `os`: In-built Python module used to interact with the operating system.
- `config`: Local `config` file containing necessary configurations.

## Classes

### Display

This is the main class responsible for creating and displaying the graph.

- **Attributes:**
    
    - `nb_graphs`: The number of graphs to be displayed.
    - `figure`: An instance of `go.Figure` from `plotly.graph_objs` on which the graph is drawn.
    - `generation_name`: Name of the current graph generation.
    - `nodes`: Nodes of the graph.
    - `edges`: Edges of the graph.
    - `nodes_color`, `edges_color`: The colors used for the nodes and edges.
    - `nodes_size`, `edges_width`: The sizes used for the nodes and the edges.
    - `save_image_path`: The path to save the generated graph image.
- **Methods:**
    
    - `__init__(nb_graphs_p, generation_name_p, node_width_p = 15, edge_width_p = 2, node_color_p = "red", edge_color_p = "blue")`: Initializes the class, sets up the figure, and configures the graph's layout.
    - `create_image_from_graph`: Creates an image of the graph in various formats (PNG, JPEG, WEBP, SVG, JSON) and saves it to the disk.
    - `process_graph(graph_p)`: Extracts and stores the nodes and edges from the input graph.
    - `create_figure`: Creates a scatter plot for each node and a line for each edge in the figure.
    - `remove_dupliacte_tuples(tuple_list_p)`: Removes any duplicate tuples from a given list of tuples.

## Execution

Upon execution, the script visualizes a graph with nodes and edges on a plotly figure. The nodes are represented as scatter plots and the edges as lines between these plots. The resulting graph is then saved to the disk in the desired format.

This script is typically used as a part of a larger pipeline and not directly executed by itself. The `Display` class would be instantiated and its methods called with appropriate arguments in the main script of the pipeline.

Please refer to the source code for more details on the implementation.