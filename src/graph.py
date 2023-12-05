from node import Node
import random as rd
import numpy as np
import json 
import os
import math

from config import Config


class Graph:
    def __init__(self, generation_name_p, nb_graphs_p, max_created_node_on_circle_p):
        """
        Create an instace of everything needed to create a graph.
        generation_name_p should be a string.
        nb_graphs_p should be an integer.
        """
        self.data = {}
        self.nodes = {}
        self.nb_nodes = 0
        self.nb_deactivated_nodes = 0
        self.index_resizer = 0
        self.generation_name = generation_name_p
        self.nb_graphs = f"/{str(nb_graphs_p)}"
        self.save_graph_path = Config.PLUME_DIR.value+"/data/"+self.generation_name+self.nb_graphs+"/data.json"
        self.adj_matrix = None
        self.max_created_node_on_circle = max_created_node_on_circle_p
    
    
    def create_adjency_matrix(self, nb_nodes_p):
        """
        Create the adjency matrix of the graph.
        In a square matrix, rows and columns correspond to nodes, and each element indicates whether an edge exists between them (and possibly the weight of the edge). 
        It's a direct mathematical representation for both nodes and their relationships.
        """
        # Initialize the adjency matrix with zeros
        self.adj_matrix = np.zeros((nb_nodes_p, nb_nodes_p))

        # Get the edges of the graph
        edges = self.get_edges()

        #Fill the matrix
        for edge in edges:
            u,v = edge
            self.adj_matrix[u][v] = 1
            self.adj_matrix[v][u] = 1


    def add_node(self, node_id_p, parent_p=None, edges_p=None, coordinates_p=None,  radius_p=None, active_p=True):
        """
        A node is created with the specified parameters. 
        Each node is represented as a dictionary and will be stored within another dictionary that encompasses all nodes in the graph.
        """
        self.nodes[node_id_p] = Node(node_id_p, parent_p, edges_p, coordinates_p, radius_p, active_p)
        if parent_p != None and edges_p != None:
            self.add_edge(node_id_p, parent_p)
        
        if parent_p != None:
            self.add_edge(node_id_p, parent_p)
        
        if edges_p != None:
            for edge in edges_p:
                self.add_edge(node_id_p, edge)
        self.nb_nodes += 1


    def add_edge(self, node_1_id, node_2_id):
        """
        Takes two integers (representing the nodes ids) and add respectively a child an a parent.
        """
        self.nodes[node_1_id].add_edge(node_2_id)
        self.nodes[node_2_id].add_edge(node_1_id)


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
        edges_list = []
        for node in self.nodes.values():
            for edge in node.edges:
                if edge != None:
                    edges_list.append((node.id, edge))
        return edges_list


    def get_neighbors(self, node_id_p,radius_p):
        # Calculate the distance between each node and the b
        origin = self.nodes[node_id_p]
        neighbours = []
        for node in self.nodes.values():
            distance = math.sqrt((origin.coordinates['x'] - node.coordinates['x']) ** 2 + (origin.coordinates['y'] - node.coordinates['y']) ** 2 + (origin.coordinates['z'] - node.coordinates['z']) ** 2 )
            if distance > radius_p:
                neighbours.append(node)
        return neighbours


    def create_random_graph(self, nb_nodes_p):
        """
        Create a graph based on random values. Test purposes
        """
        for i in range(nb_nodes_p):
            self.add_node(i,None,None,coordinates_p=(rd.randint(0,nb_nodes_p-1), rd.randint(0,nb_nodes_p-1)))
        for node in self.nodes:
            self.add_edge(rd.randint(0,nb_nodes_p-1), rd.randint(0,nb_nodes_p-1))


    def save_graph(self):
        """
        Save the graph in a json file. All child connections are conserved
        """
        # Create the target directory if it does not exist
        if not os.path.exists(os.path.dirname(self.save_graph_path)):
            os.makedirs(os.path.dirname(self.save_graph_path))
        
        if Config.THREE_DIMENSION_GENERATION.value:
            self.data["generation_dimension"] = '3D'
        else:
            self.data["generation_dimension"] = '2D'

        self.data['generation_type'] = Config.TYPE_OF_UNDERGROUND.value
        self.data['nodes'] = self.nodes
        
        with open(self.save_graph_path, "w") as outfile:
                json.dump(self.data, outfile, default=lambda o: o.__dict__, sort_keys=True, indent=4)
