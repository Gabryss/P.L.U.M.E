from node import Node
import random as rd
import numpy as np

RAW = False
DEFAULT_CSV_PATH = "data/csv_data/grid_data.csv"

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


    def add_node(self, node_id_p, parents_p=None, children_p=None, coordinates_p=None, active_p=False, grid_coordinates_p=None):
        """
        Create a node with the given parameters. The node by itself is a dictionary and will be
        stored in a dictionary that contains all the nodes of the graph.
        """
        self.nodes[node_id_p] = Node(node_id_p, parents_p, children_p, coordinates_p, active_p, grid_coordinates_p)
        self.grid[grid_coordinates_p[0]][grid_coordinates_p[1]] = node_id_p
        self.num_nodes += 1
        print(self.grid)


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

    
    def get_possible_new_nodes(self, node_ip):
        """
        Get a list of possible coordinates for new nodes
        """
        node = self.nodes[node_ip]
        possible_coordinates = []

        # Increase the grid in case the algorithm is close to a border. Update the coordinates
        if node.grid_coordinates[0] + 1 >= self.grid.shape[0] or node.grid_coordinates[0] - 1 <= 0 or node.grid_coordinates[1] + 1 >= self.grid.shape[0] or node.grid_coordinates[1] -1 <= 0:
            self.grid = np.pad(self.grid, ((1,1),(1,1)), mode='constant', constant_values=0)
            for node in self.nodes:
                node = self.nodes[node]
                node.grid_coordinates[0] += 1
                node.grid_coordinates[1] += 1

        # Check up
        if self.grid[node.grid_coordinates[0]][node.grid_coordinates[1] + 1] == 0:
            possible_coordinates.append([node.grid_coordinates[0], node.grid_coordinates[1] + 1])
        
        # Check down
        if self.grid[node.grid_coordinates[0]][node.grid_coordinates[1] - 1] == 0:
            possible_coordinates.append([node.grid_coordinates[0], node.grid_coordinates[1] - 1])

        # Check right
        if self.grid[node.grid_coordinates[0] + 1][node.grid_coordinates[1]] == 0:
            possible_coordinates.append([node.grid_coordinates[0] + 1, node.grid_coordinates[1]])

        # Check left
        if self.grid[node.grid_coordinates[0] - 1][node.grid_coordinates[1]] == 0:
            possible_coordinates.append([node.grid_coordinates[0] - 1, node.grid_coordinates[1]])

        return possible_coordinates


    def save_grid(self):
        """
        using numpy library, save the actual state of the grid in a csv file.
        """
        np.savetxt(DEFAULT_CSV_PATH, self.grid, delimiter=",", fmt='%s')