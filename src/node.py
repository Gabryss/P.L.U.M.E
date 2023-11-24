import json

class Node:
    def __init__(self, node_id_p, parent_p=None, edges_p=None, coordinates_p=[0.0,0.0,0.0], radius_p=None, active_p=False):
        self.id = node_id_p
        self.parent = parent_p if parent_p is not None else None
        self.edges = edges_p if edges_p is not None else [self.parent]
        self.coordinates = {
            'x': coordinates_p[0] if coordinates_p is not None else 0.0,
            'y': coordinates_p[1] if coordinates_p is not None else 0.0,
            'z': coordinates_p[2] if coordinates_p is not None else 0.0,
        }
        self.radius = radius_p if radius_p is not None else 1.0
        self.active = active_p if active_p is not None else False

    def __repr__(self):
        return (f"Node(ID: {self.id}, Parents: {self.parent}, Edges: {self.edges}, "
                f"Coordinates: {self.coordinates}, Radius: {self.radius}, Active: {self.active})")

    def set_parent(self, parent_p):
        self.parent = parent_p
    
    def get_parent(self):
        return self.parent
    
    def has_parent(self):
        if self.parent:
            return True
        else:
            return False
    
    def add_edge(self, edge_p):
        self.edges.append(edge_p)
    
    def set_edges(self, edges_p):
        self.edges = edges_p
    
    def get_edges(self):
        return self.edges
    
    def set_coordinates(self, coordinates_p):
        self.coordinates = coordinates_p

    def get_list_coordinates(self):
        return [self.coordinates['x'], self.coordinates['y'], self.coordinates['z']]
    
    def get_coordinates(self):
        return self.coordinates

    def get_radius(self):
        return self.radius
    
    def set_radius(self, radius_p):
        self.radius = radius_p
    
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)