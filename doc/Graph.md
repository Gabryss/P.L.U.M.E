A class used to represent a Graph structure containing a set of nodes with parent-child relationships.

## Attributes

- `nodes` : dict. A dictionary where each key-value pair represents a node id and the associated Node object respectively.
- `num_nodes` : int. The total number of nodes present in the graph.
- `grid` : numpy.array. A 2D array representing the spatial positioning of nodes. Node ids are stored at their corresponding grid position.
- `grid_size` : int. The size of the grid on which nodes are placed.
- `nb_deactivated_nodes` : int. The number of deactivated nodes in the graph.
- `index_resizer` : int. An index that tracks the number of times the grid has been resized.
- `generation_name` : str. The name associated with the current graph generation.
- `nb_graphs` : str. The number of graphs created so far.
- `save_grid_path` : str. The path where the current state of the grid is saved as a .csv file.
- `save_graph_path` : str. The path where the current graph structure is saved as a .json file.

## Methods

### `__init__(self, grid_size_p, generation_name_p, nb_graphs_p)`

Creates an instance of everything needed to create a graph. Initializes all class attributes and determines the paths where the grid and the graph structure will be saved.

### `add_node(self, node_id_p, parents_p=None, children_p=None, coordinates_p=None, active_p=False, grid_coordinates_p=None)`

Creates a node with the given parameters. The node by itself is a dictionary and will be stored in a dictionary that contains all the nodes of the graph.

### `add_edge(self, parent_id, child_id)`

Takes two integers (representing the nodes ids) and adds a parent-child relationship between them.

### `set_coordinates(self, node_id, coordinates)`

Sets the coordinates for the given node.

### `activate(self, node_id)`

Activates a node, changing its active state to True.

### `deactivate(self, node_id)`

Deactivates a node, changing its active state to False.

### `get_node(self, node_id)`

Returns a node object based on the given node_id.

### `get_nodes(self)`

Returns all node objects in the graph.

### `get_edges(self)`

Returns all edges in the graph. Each edge is represented as a tuple (parent_id, child_id).

### `get_neighbors(self, node_id)`

Returns all neighbor nodes of the given node_id. Neighbors are children of the node.

### `shortest_path(self, source_id, destination_id)`

Finds the shortest path from the source node to the destination node.

### `degree(self, node_id)`

Returns the degree of a node. The degree is the total number of parents and children the node has.

### `minimum_spanning_tree(self, start_node_id)`

Finds the minimum spanning tree of the graph starting from the given node_id.

### `strongly_connected_components(self)`

Finds the strongly connected components of the graph.

### `create_random_graph(self, nb_nodes_p)`

Creates a graph based on random values for test purposes.

### `get_grid_neighbours(self, node_id_p)`

Gets the neighbours of a node based on the 2d grid.

### `check_edge(self, node, direction="All")`

Checks if the node is close to an edge. If the node is close to an edge, increases the size of the grid by 1 on every direction.

### `increase_grid_size(self)`

Increases the grid size on each side.

### `check_empty_safe(self, node, direction=["Left", "Right", "Up", "Down"])`

Checks if there are empty space nodes around the input node and returns a list of possible coordinates.

### `check_neighboors_safe(self, node, direction=["Left", "Right", "Up", "Down"])`

Checks if there are neighbors nodes around the input node and returns a list of neighbors coordinates.

### `get_possible_new_nodes(self, node_ip)`

Gets a list of possible coordinates for new nodes.

### `get_node_coordinates_based(self, list_of_coordinates=None)`

Gets the node or nodes based on the input coordinates.

### `save_grid(self)`

Using numpy library, saves the actual state of the grid in a csv file.

### `save_graph(self)`

Saves the graph in a json file. All child connections are conserved.