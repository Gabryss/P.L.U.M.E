from node import Node

class Graph:
    def __init__(self):
        self.nodes = {}
        self.num_nodes = 0

    def add_node(self, node_id_p, parents_p=None, children_p=None, coordinates_p=None, active_p=False):
        """
        Create a node with the given parameters. The node by itself is a dictionary and will be
        stored in a dictionary that contains all the nodes of the graph.
        """
        
        # Create a new node
        node = {}
        node['id'] = node_id_p
        node['parents'] = parents_p if parents_p is not None else []
        node['children'] = children_p if children_p is not None else []
        node['coordinates'] = {
            'x': coordinates_p[0] if coordinates_p is not None else 0.0,
            'y': coordinates_p[1] if coordinates_p is not None else 0.0
        }
        node['active'] = active_p
        
        # Add the node to the graph
        self.nodes[node['id']] = node
        self.num_nodes += 1

    def add_edge(self, parent_id, child_id):
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
           
