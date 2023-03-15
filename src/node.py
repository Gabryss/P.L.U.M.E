import json

class Node:
    def __init__(self, node_id_p, parents_p=None, children_p=None, coordinates_p=[0.0,0.0], active_p=False, grid_coordinates_p=None):
        self.id = node_id_p
        self.parents = parents_p if parents_p is not None else []
        self.children = children_p if children_p is not None else []
        self.coordinates = {
            'x': coordinates_p[0] if coordinates_p is not None else 0.0,
            'y': coordinates_p[1] if coordinates_p is not None else 0.0
        }
        self.active = active_p if active_p is not None else False
        self.grid_coordinates = grid_coordinates_p if grid_coordinates_p is not None else [0,0]

    def add_parent(self, parent_id):
        self.parents.append(parent_id)

    def add_child(self, child_id):
        self.children.append(child_id)

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_active(self):
        return self.active
    
    def get_parents(self):
        return self.parents
    
    def get_children(self):
        return self.children
    
    def get_coordinates(self):
        return self.coordinates
    
    def has_parents(self):
        return len(self.parents) > 0
    
    def has_children(self):
        return len(self.children) > 0
    
    def shortest_path(self, destination_id, graph):
        visited = set()
        queue = [(self.id, [self.id])]
        while queue:
            (vertex, path) = queue.pop(0)
            if vertex == destination_id:
                return path
            for node in graph[vertex]:
                if node not in visited:
                    visited.add(node)
                    queue.append((node, path + [node]))
        return None
    
    def get_list_coordinates(self):
        return [self.coordinates['x'], self.coordinates['y']]
    
    # def __json__(self):
    #     return {"id": self.id, 
    #             "parents": self.parents, 
    #             "children": self.children,
    #             "coordinates": self.coordinates,
    #             "active": self.active,
    #             "grid_coordinates": self.grid_coordinates}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
