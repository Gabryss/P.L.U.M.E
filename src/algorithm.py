import random as rd
from tools import Tools
import numpy as np


class Algorithm():
    
    def __init__(self):
        self.iterations = 0
        self.stop_algorithm = False


    def probabilistic(self, graph_p, nb_iterations):
        """
        With a given number of iteration/or once all nodes are dead, create a graph based on the invert of Manhattan distance.
        """

        while self.iterations < nb_iterations and not self.stop_algorithm:
            print("\n\nIteration number: ", self.iterations)

            for node in list(graph_p.nodes):
                # print(graph_p.nodes)
                node = graph_p.nodes[node]

                # Check if the node is active
                if not node.active:
                    continue
                
                # Check if new nodes are possibles among neighbours
                probabilities=[]
                possibilities = graph_p.get_possible_new_nodes(node.id)

                # Check if possible new nodes
                if len(possibilities) == 0:
                    continue
                    
                else:
                    print("node id :", node.id, "possibilities :", possibilities)
                    # Calculate the probability according to the distance to the original node
                    for possibility in possibilities:
                        probabilities.append(1 / len(possibilities))
                    print(probabilities)
                    # Apply probability to our list of created nodes
                    nb_created_nodes_choice = rd.choice(range(len(possibilities)))
                    # coordinates_choice = rd.sample(possibilities, nb_created_nodes_choice)
                    
                    # coordinates_choice = rd.choices(possibilities, weights=probabilities, k=nb_created_nodes_choice)
                    index_list = np.random.choice(range(len(possibilities)), nb_created_nodes_choice, replace=False, p=probabilities)
                    coordinates_choice = []
                    for index in index_list:
                        coordinates_choice.append(possibilities[index])

                    # Create new nodes
                    for i in range(nb_created_nodes_choice):
                        print(graph_p.grid)
                        coord = coordinates_choice.pop()
                        child_graph_coordinates = self.calculate_right_graph_coordinates(node, coord)
                        
                        graph_p.add_node(graph_p.num_nodes+1, [node.id], None, coordinates_p=child_graph_coordinates, active_p=True, grid_coordinates_p=coord)
                        graph_p.add_edge(node.id, graph_p.nodes[graph_p.num_nodes].id)
                        print("Distance from parent",node.id, " to child ", graph_p.num_nodes, " is ", self.node_manhattan_distance(node,graph_p.nodes[graph_p.num_nodes]))

                    graph_p.nodes[node.id].active = False
                    graph_p.nb_deactivated_nodes += 1

                    # Check if all nodes are dead
                    if graph_p.nb_deactivated_nodes == len(graph_p.nodes):
                        self.stop_algorithm = True
            self.iterations += 1

        self.loopclosure(graph_p)


    def loopclosure(self, graph_p):
        print("Post processing...")
        directions = ["Left", "Right", "Up", "Down"]

        for node_id in graph_p.nodes:
            node = graph_p.nodes[node_id]

            # Check for edges
            walls = graph_p.check_edge(node)
            if walls:
                possible_neighbors = directions.copy()
                for direction in directions:
                    wall = graph_p.check_edge(node, direction)
                    if wall:
                        possible_neighbors.remove(direction)
            
            # Check neighbors on the remaining coordinates
            neighbors_coordinates = graph_p.check_neighbors_safe(node)
            print("DEBUGGING MODE ",neighbors_coordinates)

            neighbors = graph_p.get_neighbors_node_coordinates_based(neighbors_coordinates)

            if neighbors == None:
                continue

            else:
                for neighbor in neighbors:
                    if node.id in neighbor.children or node.id in neighbor.parents:
                        continue
                    elif neighbor.id in node.children or neighbor.id in node.parents:
                        continue
                    
                    else:
                        if rd.randint(0,1):
                            node.children.append(neighbor.id)


    def voronoi(self, graph_p):
        pass

    def lattice_fibo(self, graph_p):
        pass

    def node_manhattan_distance(self, node1, node2):
        """
        Calculate and return the Manhattan distance between two nodes.
        |x1-x2|+|y1-y2|
        """
        manhattan_distance = abs(node1.coordinates['x'] - node2.coordinates['x']) + abs(node1.coordinates['y'] - node2.coordinates['y'])
        return manhattan_distance
    

    def manhattan_distance(self, coord1, coord2):
        """
        Calculate and return the Manhattan distance between two nodes.
        |x1-x2|+|y1-y2|
        """
        manhattan_distance = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])
        return manhattan_distance
    

    # Tools

    def calculate_right_graph_coordinates(self, parent_node_p, grid_coordinates_p):
        """
        Based on the parent coordinates and the new child coordinates, return the coordinates of the child on the graph
        """
        # Get parent coordinate
        parent_grid_coordinates = parent_node_p.grid_coordinates
        parent_graph_coordinates = parent_node_p.get_list_coordinates()

        # Get the transform between the parent and the child
        difference_grid_coordinates = Tools().substract_list(grid_coordinates_p, parent_grid_coordinates)
        difference_grid_coordinates[0] = -difference_grid_coordinates[0]
        difference_grid_coordinates.reverse()

        # Get the child graph coordinates
        child_graph_coordinates = [parent_graph_coordinates[0]+difference_grid_coordinates[0], parent_graph_coordinates[1]+difference_grid_coordinates[1]]
        return child_graph_coordinates

    