import random as rd
from tools import Tools
import numpy as np

class Algorithm():
    
    def __init__(self, graph_p, min_nodes_p = 4, loop_closure_probability_p = 10):
        self.graph = graph_p
        self.iterations = 0
        self.min_nodes = min_nodes_p
        self.loop_closure_probability = loop_closure_probability_p
        self.angles = np.arange(360)

    def algorithm(self, selected_algorithm="gaussian_perlin"):
        """
        Main algorithm generation
        """
        if selected_algorithm=="gaussian_perlin":
            first_node_probability = self.perlin_distribution_circle()
    

    def gaussian_perlin(self):
        """
        Execute the Gaussian-Perlin algorithm
        """
        for i in range(self.min_nodes):
            probability_array = np.zeros((3,360))
            probability_final = np.zeros((1,360))

            probability_array[0] = self.gaussian_distribution_circle()
            probability_array[1] = self.gaussian_distribution_circle()
            probability_array[2] = self.perlin_distribution_circle()
            for i in range(360):
                probability_final[0][i] = (probability_array[0][i]+probability_array[1][i]+probability_array[2][i])/3
            # Choose an angle based on the distribution
            chosen_angle = np.random.choice(self.angles, p=probability_final)


    def gaussian_distribution_circle(self, direction_p):
        """
        Return a Gaussian distribution array based on a given direction (degree).
        The distribution is returned in a list of 360 elements (1 element per degree).
        """

        pass


    def perlin_distribution_circle(self, direction_p):
        """
        Return a Perlin distribution array based on a given direction (degree).
        The distribution is returned in a list of 360 elements (1 element per degree).
        """
        pass


    def loop_closure(self):
        """
        Post processing loop closure creation
        """
        pass


    def voronoi(self):
        pass


    def lattice_fibo(self):
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

    