import json

class Node:
    def __init__(self, node_id_p, parents_p=None, edges_p=None, coordinates_p=[0.0,0.0], active_p=False):
        self.id = node_id_p
        self.parents = parents_p if parents_p is not None else None
        self.edges = edges_p if edges_p is not None else [self.parents]
        self.coordinates = {
            'x': coordinates_p[0] if coordinates_p is not None else 0.0,
            'y': coordinates_p[1] if coordinates_p is not None else 0.0
        }
        self.active = active_p if active_p is not None else False

    def add_parent(self, parent_id_p):
        self.parents.append(parent_id_p)
    
    def set_parent(self, parent_p):
        self.parents = parent_p
    
    def get_parents(self):
        return self.parents
    
    def has_parents(self):
        if self.parents:
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
        return [self.coordinates['x'], self.coordinates['y']]
    
    def get_coordinates(self):
        return self.coordinates
    
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)