import random as rd
import numpy as np
import math
from noise import snoise2
from config import Config

class Algorithm():
    
    def __init__(self, graph_p, min_nodes_p = 4, loop_closure_probability_p = 10):
        self.graph = graph_p
        self.iterations = 0
        self.min_nodes = min_nodes_p
        self.loop_closure_probability = loop_closure_probability_p
        self.angles = np.arange(360)
        self.current_node_index=1
        self.stop_algorithm = False


    def algorithm(self, selected_algorithm="gaussian_perlin"):
        """
        Main algorithm generation
        Starting node already defined
        """
        if selected_algorithm=="gaussian_perlin":
            # Nodes around the starting node
            first_node_probability = self.perlin_distribution_circle()
            nb_nodes = rd.randint(2, self.graph.max_created_node_on_circle)
            for i in range(nb_nodes):
                chosen_angle = np.random.choice(self.angles, p=first_node_probability)
                self.graph.add_node(node_id_p=i+1, parent_p=0, coordinates_p=self.get_coordinates_on_circle(radius_p=self.graph.nodes[0].radius, theta_p=chosen_angle, index_p=0), radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value), active_p=True)
                self.graph.nodes[0].add_edge(i+1)
            # The graph
            self.gaussian_perlin()
        
        if selected_algorithm == "mine":
            # Nodes around the starting node
            first_node_probability = self.perlin_distribution_circle()
            chosen_angle = np.random.choice(self.angles, p=first_node_probability)
            self.graph.add_node(node_id_p=1, parent_p=0, coordinates_p=self.get_coordinates_on_circle(radius_p=self.graph.nodes[0].radius, theta_p=chosen_angle, index_p=0), radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value), active_p=True)
            self.graph.nodes[0].add_edge(1)
            # The graph
            self.mine()


    def gaussian_perlin(self):
        """
        Execute the Gaussian-Perlin algorithm
        """
        self.current_node_index = self.graph.nb_nodes-1
        for i in range(self.min_nodes):           
            current_node = self.graph.nodes[self.current_node_index]
            
            parent_node = self.graph.nodes[self.graph.nodes[current_node.id].parent]
            angle_parent = self.calculate_angle(parent_node, current_node)

            if parent_node.id:
                grand_parent_node = self.graph.nodes[self.graph.nodes[parent_node.id].parent]
                angle_grand_parent = self.calculate_angle(grand_parent_node, parent_node)
                
                probability_array = np.zeros((3,360))
                probability_final = np.zeros((1,360))

                probability_array[0] = self.gaussian_distribution_circle(360-angle_parent)
                probability_array[1] = self.gaussian_distribution_circle(360-angle_grand_parent)
                probability_array[2] = self.perlin_distribution_circle()
            
                for i in range(360):
                    probability_final[0][i] = (probability_array[0][i]+probability_array[1][i])/2


            else:
                # probability_array = np.zeros((1,360))
                probability_final = np.zeros((1,360))

                probability_final[0] = self.gaussian_distribution_circle(360-angle_parent)
                # probability_array[1] = self.perlin_distribution_circle()
            
                # for i in range(360):
                #     probability_final[0][i] = (probability_array[0][i]+probability_array[1][i])/2
            
            # Choose an angle based on the distribution
            nb_nodes = rd.randint(0,self.graph.max_created_node_on_circle)
            for i in range(nb_nodes):
                chosen_angle = np.random.choice(self.angles, p=probability_final[0])
                self.graph.add_node(node_id_p=self.graph.nb_nodes, parent_p=self.current_node_index, coordinates_p=self.get_coordinates_on_circle(radius_p=self.graph.nodes[self.current_node_index].radius, theta_p=chosen_angle, index_p=self.current_node_index), radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value), active_p=True)
                        
            self.current_node_index += 1

            if self.current_node_index >= len(self.graph.nodes):
                self.current_node_index -= 1
                continue


    def gaussian_distribution_circle(self, direction_p):
        """
        Return a Gaussian distribution array based on a given direction (degree).
        The distribution is returned in a list of 360 elements (1 element per degree).
        """
        direction = direction_p
        # Convert the input angle to a value between 0 and 1
        direction = direction % 360 / 360.0

        # Create an array of angles from 0 to 1
        angles = np.linspace(0, 1, 360)

        # Generate a Gaussian distribution centered at the input angle
        gaussian_values = np.exp(-0.5 * ((angles - direction) / Config.STANDARD_DEVIATION.value) ** 2)

        # Normalize the values so they sum to 1
        gaussian_values = gaussian_values / gaussian_values.sum()

        return gaussian_values


    def perlin_distribution_circle(self):
        """
        Return a Perlin distribution.
        The distribution is returned in a list of 360 elements (1 element per degree).
        """
        scale=rd.uniform(0.1, Config.MAX_SCALE.value)
        octaves=rd.uniform(0.1, Config.MAX_OCTAVES.value)
        persistence=rd.uniform(0.1, Config.MAX_PERSISTENCE.value)
        lacunarity=rd.uniform(0.1, Config.MAX_LACUNARITY.value)
        x = np.linspace(0, 1, 360)
        y = np.linspace(0, 1, 360)
        
        # Create an empty array to store the noise values
        noise_values = np.empty(360)

        # Generate perlin noise for each point in the circle
        for i in range(360):
            noise_values[i] = snoise2(x[i]*scale, y[i]*scale, 1, octaves, persistence, lacunarity)

        # Normalize the values so they sum to 1
        noise_values = noise_values - noise_values.min()  # Make the values positive
        noise_values = noise_values / noise_values.sum()  # Normalize to sum to 1
        return noise_values


    def mine(self):
        """
        MINE CONTEXT
        Create a graph that looks like a mine structure
        """
        print("In mine algo")
        origin = list(self.graph.nodes.values())[-1]
        self.current_node_index = self.graph.nb_nodes-1
        number_nodes = self.graph.nb_nodes
        print(number_nodes)
        origin = self.graph.nodes[self.current_node_index]

        while number_nodes < Config.DEFAULT_MIN_NODES.value:
            nb_branch = rd.randint(1,3)
            for i in range(nb_branch):
                # Create a main branch
                branch = self.mine_add_main_branch(origin)
                if branch:
                    # Add sub branches (harvesting sites) to main branch
                    break_point_sub = self.mine_add_sub_branches(branch)
                    if break_point_sub:
                        continue
                    else:
                        return 1
                else:
                    return 1
                
            if not Config.THREE_DIMENSION_GENERATION.value:
                print("yes")
                return 1
            
            else:
                print("no")
                origin = self.graph.add_node(node_id_p=self.graph.nb_nodes, parent_p= origin.id, coordinates_p=(origin.coordinates['x'], origin.coordinates['y'], origin.coordinates['z'] - Config.Z_AXIS_LAYER_STEP.value ), radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value))
            print("New wave", number_nodes)


    def mine_add_main_branch(self, origin_p):
        """
        MINE CONTEXT
        Create a main branch based on the position of the origin
        """
        print("In main branch")
        size_branch = rd.randint(2,10)
        branch = []
        last_node = None
        shift = None
        for i in range(size_branch):
            if i == 0:
                chosen_angle = np.random.choice(self.angles)
                shift = (rd.randint(1,5)*rd.random()*([-1,1][rd.randrange(2)]), rd.randint(1,5)*rd.random()*([-1,1][rd.randrange(2)]))
                last_node = self.graph.add_node(node_id_p=self.graph.nb_nodes, parent_p=origin_p.id, coordinates_p=(origin_p.coordinates['x']+shift[0],origin_p.coordinates['y']+shift[1],origin_p.coordinates['z']), radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value), active_p=True)
                branch.append(last_node)
            else:
                last_node = self.graph.add_node(node_id_p=self.graph.nb_nodes, parent_p=last_node.id, coordinates_p=(origin_p.coordinates['x']+shift[0]*i,origin_p.coordinates['y']+shift[1]*i,origin_p.coordinates['z']), radius_p=rd.uniform(1.0, Config.MAX_RADIUS_NODE.value), active_p=True)
                branch.append(last_node)
            # Check if number of desired nodes reached
            if self.graph.nb_nodes >= Config.DEFAULT_MIN_NODES.value:
                return 0
        return branch

    def mine_add_sub_branches(self, branch_p):
        """
        MINE CONTEXT
        Add small branches along an given main branch (list of nodes)
        """
        print("In sub branch")
        for main_branch_node in branch_p:
            # Add sub branches of random size
            size_branch = rd.randint(0,5)
            last_node = None

            for i in range(size_branch):
                # 2D Rotation matrix
                coord_x = main_branch_node.coordinates['x'] + 1
                coord_y = main_branch_node.coordinates['y'] + 1
                # coord_x = main_branch_node.coordinates['x'] * math.cos(math.pi/2) - main_branch_node.coordinates['y'] * math.sin(math.pi/2)
                # coord_y = main_branch_node.coordinates['x'] * math.sin(math.pi/2) + main_branch_node.coordinates['y'] * math.cos(math.pi/2)
                if i == 0:
                    # Create a node from the main branch node
                    # self.graph.add_node(node_id_p=self.graph.nb_nodes, parent_p=main_branch_node.id, coordinates_p=self.get_coordinates_on_circle(radius_p=self.main_branch_node.radius, theta_p=45, index_p=self.main_branch_node.id), radius_p=0.5, active_p=True)
                    last_node = self.graph.add_node(node_id_p=self.graph.nb_nodes, parent_p=main_branch_node.id, coordinates_p=(coord_x,coord_y,main_branch_node.coordinates['z']), radius_p=0.5, active_p=True)
                else:
                    # Extend the sub branch
                    last_node = self.graph.add_node(node_id_p=self.graph.nb_nodes, parent_p=last_node.id, coordinates_p=(coord_x+i, coord_y+i, main_branch_node.coordinates['z']), radius_p=0.5, active_p=True)

                if self.graph.nb_nodes >= Config.DEFAULT_MIN_NODES.value:
                    return 0
        return 1


    def loop_closure(self):
        """
        Post processing loop closure creation
        """
        pass

   
    def get_coordinates_on_circle(self, radius_p, theta_p, index_p):
        """
        Return the coordinates of a point in a circle based on the origin's coordinate and the radius of the circle as well as it's angle.
        """
        radius = radius_p
        theta = theta_p
        index = index_p
        node = self.graph.nodes[index]
        x = node.coordinates['x'] + radius * math.cos(theta)
        y = node.coordinates['y'] + radius * math.sin(theta)

        # 3D generation
        if Config.THREE_DIMENSION_GENERATION.value:
            z_layer_probability = Config.Z_AXIS_LAYER_PROB.value/100
            layer_choice = rd.choices(population=[True,False], weights=[z_layer_probability,1-z_layer_probability])
            if layer_choice[0]:
                z = node.coordinates['z'] - Config.Z_AXIS_LAYER_STEP.value
                x *= Config.Z_AXIS_STEP_DOWN_XY_SHIFT.value
                y *= Config.Z_AXIS_STEP_DOWN_XY_SHIFT.value
            else:
                # z = node.coordinates['z']
                z = node.coordinates['z'] + rd.gauss(Config.Z_AXIS_GAUSSIAN_MEAN.value, 0.1)
        else:
            z = 0.0
        return list((x,y,z))


    def calculate_angle(self, parent_node_p, current_node_p):
        """
        Calculate the angle (in degrees) between the positive x-axis and the line connecting the origin to a point on the circle.
        
        Args:
        parent_node_p (node object): The parent node, used to fetch the coordinate of the circle's center.
        current_node_p (node object): The current node, used to fetch the coordinate of the circle's center.


        Returns:
        float: The angle in degrees.
        """
        parent_node = parent_node_p
        current_node = current_node_p
        
        # Compute the difference between point coordinates and the center of the circle
        diff_x = current_node.coordinates['x'] - parent_node.coordinates['x']
        diff_y = current_node.coordinates['y'] - parent_node.coordinates['y']

        # Compute the angle from the difference in the x and y positions
        # Note: we use math.atan2 because it retains the sign of both inputs,
        # which allows it to return values in all four quadrants.
        angle_radians = math.atan2(diff_y, diff_x)

        # Convert the angle to degrees
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees


    def node_manhattan_distance(self, node1, node2):
        """
        Calculate and return the Manhattan distance between two nodes.
        |x1-x2|+|y1-y2|
        """
        manhattan_distance = abs(node1.coordinates['x'] - node2.coordinates['x']) + abs(node1.coordinates['y'] - node2.coordinates['y']) + abs(node1.coordinates['z'] - node2.coordinates['z'])
        return manhattan_distance


    def manhattan_distance(self, coord1, coord2):
        """
        Calculate and return the Manhattan distance between two nodes.
        |x1-x2|+|y1-y2|
        """
        manhattan_distance = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1]) + abs(coord1[2] - coord2[2])
        return manhattan_distance

    