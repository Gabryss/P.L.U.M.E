from node import Node
import random as rd
import numpy as np
import json 

DEFAULT_CSV_PATH = "data/raw_data/grid_data.csv"
DEFAULT_GRAPH_PATH = "data/raw_data/data.json"

class Graph:
    def __init__(self, grid_size_p):
        """
        Create an instace of everything needed to create a graph.
        grid_size_p should be an integer.
        """
        self.nodes = {}
        self.num_nodes = 0
        self.grid = np.zeros((grid_size_p, grid_size_p), dtype=object)
        self.grid_size = grid_size_p
        self.nb_deactivated_nodes = 0
        self.index_resizer = 0


    def add_node(self, node_id_p, parents_p=None, children_p=None, coordinates_p=None, active_p=False, grid_coordinates_p=None):
        """
        Create a node with the given parameters. The node by itself is a dictionary and will be
        stored in a dictionary that contains all the nodes of the graph.
        """
        
        if self.grid[grid_coordinates_p[0]][grid_coordinates_p[1]] != 0:
            print("Coordinates", grid_coordinates_p)
            print("Node ID", node_id_p)
            print("Parent ID", parents_p)
            print("Parent coordinates", self.nodes[parents_p[0]].grid_coordinates)
            raise AssertionError
        else:
            self.nodes[node_id_p] = Node(node_id_p, parents_p, children_p, coordinates_p, active_p, grid_coordinates_p)
            self.grid[grid_coordinates_p[0]][grid_coordinates_p[1]] = node_id_p
            self.num_nodes += 1


    def add_edge(self, parent_id, child_id):
        """
        Takes two integers (representing the nodes ids) and add respectively a child an a parent.
        """
        self.nodes[parent_id].add_child(child_id)
        self.nodes[child_id].add_parent(parent_id)


    def set_coordinates(self, node_id, coordinates):
        self.nodes[node_id].set_coordinates(coordinates)


    def activate(self, node_id):
        self.nodes[node_id].activate()


    def deactivate(self, node_id):
        self.nodes[node_id].deactivate()


    def get_node(self, node_id):
        return self.nodes[node_id]


    def get_nodes(self):
        return self.nodes.values()


    def get_edges(self):
        edges = []
        for node in self.nodes.values():
            for child_id in node.children:
                edges.append((node.id, child_id))
        return edges
    

    def get_neighbors(self, node_id):
        node = self.nodes[node_id]
        return [self.nodes[child_id] for child_id in node.childs]


    def shortest_path(self, source_id, destination_id):
        return self.nodes[source_id].shortest_path(destination_id, self.nodes)


    def degree(self, node_id):
        return len(self.nodes[node_id].parents) + len(self.nodes[node_id].children)


    def minimum_spanning_tree(self, start_node_id):
        visited = set()
        mst = []
        node = self.nodes[start_node_id]
        stack = [(None, node)]
        while stack:
            parent, node = stack.pop()
            if node.id in visited:
                continue
            visited.add(node.id)
            if parent:
                mst.append((parent.id, node.id))
            for child_id in node.children:
                stack.append((node, self.nodes[child_id]))
        return mst


    def strongly_connected_components(self):
        visited = set()
        components = []
        for node_id in self.nodes:
            if node_id in visited:
                continue
            component = []
            stack = [node_id]
            while stack:
                node = self.nodes[stack.pop()]
                if node.id in visited:
                    continue
                visited.add(node.id)
                component.append(node.id)
                for parent_id in node.parents:
                    stack.append(parent_id)
            components.append(component)
        return components


    def cycles(self):
        visited = set()
        cycles = []
        for node_id in self.nodes:
            if node_id in visited:
                continue
            stack = [(None, node_id)]
    

    def create_random_graph(self, nb_nodes_p):
        """
        Create a graph based on random values. Test purposes
        """
        for i in range(nb_nodes_p):
            self.add_node(i,None,None,coordinates_p=(rd.randint(0,nb_nodes_p-1), rd.randint(0,nb_nodes_p-1)))
        for node in self.nodes:
            self.add_edge(rd.randint(0,nb_nodes_p-1), rd.randint(0,nb_nodes_p-1))


    def get_grid_neighbours(self, node_id_p):
        """
        Get the neigbhours based on the 2d grid
        """
        neighbours = []
        node = self.nodes[node_id_p]
        x, y = -1, 0
        for i in range(2):
            neighbours.append(self.grid[node.grid_coordinates[0] + x][node.grid_coordinates[1] + y])
            neighbours.append(self.grid[node.grid_coordinates[0] + y][node.grid_coordinates[1] + x])
            x, y = 1, 0
        for neighbour in neighbours:
            if neighbour == 0:
                neighbours.remove(neighbour)
        return neighbours
    

    def check_edge(self, node, direction="All"):
        """
        Check if the node is close to an edge.
        If the node is close to an edge, increase the size of the grid by 1 on every direction
        Return 1 if there is a wall, else return 0
        """
        if direction == "All":
            if node.grid_coordinates[0] >= self.grid.shape[0] - 1 or node.grid_coordinates[0] <= 0 or node.grid_coordinates[1] >= self.grid.shape[1] - 1 or node.grid_coordinates[1] <= 0:
                return 1
            else:
                return 0
        
        if direction == "Down":
            if node.grid_coordinates[0] >= self.grid.shape[0] - 1:
                return 1
            else:
                return 0
        
        if direction == "Up":
            if node.grid_coordinates[0] <= 0 :
                return 1
            else:
                return 0
            
        if direction == "Right":
            if node.grid_coordinates[1] >= self.grid.shape[1] - 1 :
                return 1
            else:
                return 0
        
        if direction == "Left":
            if node.grid_coordinates[1] <= 0 :
                return 1
            else:
                return 0


    def increase_grid_size(self):
        """
        Increase the grid size on each side.
        The coordinates are also updated to match the position on the previous grid 
        """
        self.grid = np.pad(self.grid, ((1,1),(1,1)), mode='constant', constant_values=0)
        self.grid_size = self.grid.ndim
        self.index_resizer += 1

        # Updating the coodinates according to the new grid
        for node in self.nodes:
            node = self.nodes[node]
            node.grid_coordinates[0] += 1
            node.grid_coordinates[1] += 1

        print("Grid rezised, new grid size :", self.grid.shape)
        print("Index size :", self.index_resizer)

        
    def check_empty_safe(self, node, direction=["Left", "Right", "Up", "Down"]):
        """
        Check if there are empty space nodes around the input node
        Return a list of possible coordinates
        """
        empty_space = []

        # Check right
        if "Right" in direction and self.grid[node.grid_coordinates[0]][node.grid_coordinates[1] + 1] == 0:
            empty_space.append([node.grid_coordinates[0], node.grid_coordinates[1] + 1])
        
        # Check left
        if "Left" in direction and self.grid[node.grid_coordinates[0]][node.grid_coordinates[1] - 1] == 0:
            empty_space.append([node.grid_coordinates[0], node.grid_coordinates[1] - 1])

        # Check up
        if "Up" in direction and self.grid[node.grid_coordinates[0] - 1][node.grid_coordinates[1]] == 0:
            empty_space.append([node.grid_coordinates[0] - 1, node.grid_coordinates[1]])

        # Check down
        if "Down" in direction and self.grid[node.grid_coordinates[0] + 1][node.grid_coordinates[1]] == 0:
            empty_space.append([node.grid_coordinates[0] + 1, node.grid_coordinates[1]])

        return empty_space      
    

    def check_neighboors_safe(self, node, direction=["Left", "Right", "Up", "Down"]):
        """
        Check if there are neighbors nodes around the input node
        Return a list of neighbors coordinates
        """
        possible_neighbors = []

        # Check right
        if "Right" in direction and self.grid[node.grid_coordinates[0]][node.grid_coordinates[1] + 1] != 0:
            possible_neighbors.append([node.grid_coordinates[0], node.grid_coordinates[1] + 1])
        
        # Check left
        if "Left" in direction and self.grid[node.grid_coordinates[0]][node.grid_coordinates[1] - 1] != 0:
            possible_neighbors.append([node.grid_coordinates[0], node.grid_coordinates[1] - 1])

        # Check up
        if "Up" in direction and self.grid[node.grid_coordinates[0] - 1][node.grid_coordinates[1]] != 0:
            possible_neighbors.append([node.grid_coordinates[0] - 1, node.grid_coordinates[1]])

        # Check down
        if "Down" in direction and self.grid[node.grid_coordinates[0] + 1][node.grid_coordinates[1]] != 0:
            possible_neighbors.append([node.grid_coordinates[0] + 1, node.grid_coordinates[1]])

        return possible_neighbors   


    def get_possible_new_nodes(self, node_ip):
        """
        Get a list of possible coordinates for new nodes
        """
        node = self.nodes[node_ip]
        possible_neighbors = []
        wall = self.check_edge(node)

        if wall:
            self.increase_grid_size()
        
        #   In numpy values are stored in a particular way which is: m[y][x]
        print("Node:", node.id, "stalk neighbours")
        print("Node", node.id, "coordinates", node.grid_coordinates)

        possible_neighbors = self.check_empty_safe(node)

        return possible_neighbors

    def get_node_coordinates_based(self, list_of_coordinates=None):
        """
        Get the node based on the input coordinates
        Return either a node or a list of nodes based on the input
        """
        if list_of_coordinates == None or list_of_coordinates == []:
            return None
        
        else:
            list_of_nodes = []
            for coordinates in list_of_coordinates:
                node_id = self.grid[coordinates[0]][coordinates[1]]
                node = self.nodes[node_id]
                list_of_nodes.append(node)
            return list_of_nodes


    def save_grid(self):
        """
        using numpy library, save the actual state of the grid in a csv file.
        """
        np.savetxt(DEFAULT_CSV_PATH, self.grid, delimiter=",", fmt='%s')


    def save_graph(self):
        """
        Save the graph in a json file. All child connections are conserved
        """
        with open(DEFAULT_GRAPH_PATH, "w") as outfile:
                json.dump(self.nodes, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
