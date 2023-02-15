import random as rd

class Algorithm():
    
    def __init__(self):
        pass

    def probabilistic(self, graph_p, nb_iteration):
        for i in range(nb_iteration):

            for node in list(graph_p.nodes):
                # print(graph_p.nodes)
                node = graph_p.nodes[node]
                # Check if new nodes are possibles among neighbours
                probabilities=[]
                possibilities = graph_p.get_possible_new_nodes(node.id)
                print(possibilities)


                # Check if active node
                if not node.active or len(possibilities) == 0:
                    continue
                    
                else:

                    # Calculate the probability according to the distance to the original node
                    for possibility in possibilities:
                        probabilities.append(1 / self.manhattan_distance(graph_p.nodes[1].grid_coordinates, possibility))

                    # Apply probability to our list of created nodes
                    nb_created_nodes_choice = rd.choice(range(len(possibilities)))
                    coordinates_choice = rd.choices(possibilities, weights=probabilities, k=nb_created_nodes_choice)

                    # Create new nodes
                    for i in range(nb_created_nodes_choice):
                        coord = coordinates_choice.pop()
                        correction_coordinates = self.substract_list(coord, [graph_p.grid_size//2, graph_p.grid_size//2])
                        coordinates_new_node = self.substract_list(correction_coordinates, [node.coordinates['x'],node.coordinates['y']])
                        graph_p.add_node(graph_p.num_nodes+1,None, None, coordinates_p=[node.coordinates['x'] + coordinates_new_node[0], node.coordinates['y'] + coordinates_new_node[1]], active_p=True, grid_coordinates_p=coord)
                        graph_p.add_edge(node.id, graph_p.nodes[graph_p.num_nodes].id)


                    # node.active = False


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
    
    def substract_list(self, list1, list2):
        """
        Substract two list and return the resulting list
        """
        result = []
        for i,j in zip(list1, list2):
            result.append(i-j)
        return result