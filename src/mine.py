import sys
import os
import bpy
import json
import numpy as np
import csv
import argparse

# Get the path of the PLUME directory
if os.path.dirname(__file__) not in sys.path:
   sys.path.append(os.path.dirname(__file__))

# # Fetch the blender directory
blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)




# PATH="~Document/PhD/Lava_tubes/python/P.L.U.M.E/data/raw_data/small_grid2_2023_09_25_13_25_26/0/"
# PATH="./data/raw_data/small_grid2_2023_09_25_13_25_26/0/"
PATH="./data/raw_data/grid_large_2023_11_15_15_44_42/0/"


class MineGeneration:
    def __init__(self) -> None:
        # self.generation_name = str(generation_name_p)
        # self.index = str(index_p)
        self.asset_path = "./data/mine_assets/"
        self.json_path = PATH + "data.json"
        self.grid_path = PATH + "grid_data.csv"
    #   self.path = PLUME_DIR.value+"/data/raw_data/"+self.generation_name+"/"+self.index+"/data.json"
    #   self.saved_mesh_path = PLUME_DIR.value+"/data/mesh_files/"+self.generation_name+"/"+self.index+"/mesh.obj"
        self.json_file = open(self.json_path)
        self.data = json.load(self.json_file)
        self.grid = self.import_csv(self.grid_path)

        self.obj = None
        self.mesh = None
        self.initial_cleanup()
        self.verts, self.edges = self.extract_mesh_data()
        self.rooms_placement()
        # exit()
    

    def import_csv(self, path_p):
        """
        Import csv grid into array
        """
        with open(path_p, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)

        data_array = np.array(data, dtype=int)
        return data_array
      

    def initial_cleanup(self):
        """
        Remove the default object of Blender
        """
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects['Camera'].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects['Light'].select_set(True)
        bpy.ops.object.delete()

    def extract_mesh_data(self):
        """
        Load graph data into python variables (from a dictionary)
        -Use [node_id]["coordinates"]["x"] or ["y"]
        """
        verts, edges = [], []
        for i in self.data:
            verts.append([
            self.data[i]["coordinates"]['x'],
            self.data[i]["coordinates"]['y'],
            0.0
            ])
            for edge in self.data[i]['children']:
                edges.append([
                    self.data[i]['id'],
                    edge
                ])
        return verts, edges


    def rooms_placement(self):
        """
        Place rooms to the correct position
        """
        print("Verticies \n",self.verts)
        print("Edges \n", self.edges)
        view_layer = bpy.context.view_layer

        object_collection = bpy.data.objects.items()
        node_id = 1
        

        # Choose which mesh to import based on the number of neighbours and their configuration
        for vert in self.verts:
            object_name, orientation, position = self.check_neighbours(node_id)
            bpy.ops.wm.obj_import(filepath=self.asset_path+f"{object_name}"+".obj")

            #Fetch the new added item
            added_object = list(set(bpy.data.objects.items()).symmetric_difference(set(object_collection)))[0]            
            object_collection = bpy.data.objects.items()
            
            #Transformation
            bpy.data.objects[added_object[0]].rotation_euler = (90.0*(3.14/180),0.0*(3.14/180),orientation*(3.14/180))
            bpy.data.objects[added_object[0]].location = position
            
            node_id += 1


    def check_neighbours(self, id):
        """
        Check the neigbhours nodes and their connections witht the current node
        """
        grid_coordinates = self.data[f'{id}']["grid_coordinates"]
        neighbours_list = list(dict.fromkeys(self.data[f'{id}']["children"]+self.data[f'{id}']["parents"]))
        position = (self.data[f'{id}']["coordinates"]["x"]*2, self.data[f'{id}']["coordinates"]["y"]*2, 0)
        node_y = grid_coordinates[0]
        node_x = grid_coordinates[1]
        shape = []

        print(neighbours_list)
        print(id)

        for neighbour in neighbours_list:
            if self.grid[node_y,node_x+1] == neighbour:
                shape.append('right')
            elif self.grid[node_y,node_x-1] == neighbour:
                shape.append('left')
            elif self.grid[node_y+1,node_x] == neighbour:
                shape.append('down')
            elif self.grid[node_y-1,node_x] == neighbour:
                shape.append('up')
        shape.sort()
        print(shape)

        L_shape=[['left','up'],['left','down'], ['right','down'],['up','right'],]
        [list.sort() for list in L_shape]
        print(L_shape)

        corr_shape=[['down','up'],['left','right']]
        [list.sort() for list in corr_shape]

        end_shape=[('up'),('right'), ('down'), ('left')]
        end_shape.sort()

        T_shape=[['left','up','right'], ['down', 'left', 'up'], ['left', 'down', 'right'], ['down', 'right', 'up']]
        [list.sort() for list in T_shape]

        if len(neighbours_list) == 4:
            obj_name = "X"
            orientation = 0.0
        
        elif len(neighbours_list) == 1:
            obj_name = "End"
            orientation = self.get_angle(shape[0])
        
        elif len(neighbours_list) == 3:
            obj_name = "T"
            try:
                idx = T_shape.index(shape)
                print(f"The index is: {idx}")
                orientation = (idx+1)*90
            except ValueError:
                print("The list is not found in T_shape.")

        elif len(neighbours_list) == 2:
            if shape in L_shape:
                obj_name = "L"
                try:
                    idx = L_shape.index(shape)
                    print(f"The index is: {idx}")
                    orientation = (idx+1)*90
                except ValueError:
                    print("The list is not found in L_shape.")

            else:
                obj_name = "corridor"
                if 'up' in shape:
                    orientation = 0
                else:
                    orientation = 90

        return obj_name, float(orientation), position



    def get_angle(self, orientation_p):
        """
        Return the angle in degrees of the shape's orientation
        """
        if orientation_p == 'up':
            return 0
        if orientation_p == 'right':
            return 270
        if orientation_p == 'left':
            return 90
        if orientation_p == 'down':
            return 180
            
        
if __name__ == '__main__':
   
   print(sys.argv)

#    parser = argparse.ArgumentParser(
#                                 description="PLUME project. Mesh generation based on a json file that provide data as x,y,z coordinates. Then based on the created structure, apply a circular skin around it to create the edges of the underground mesh.",
#                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
#    parser.add_argument("-index", help="Index used for the path", type=int)
#    parser.add_argument("-name", help="Name of the current graph generation", type=str)
#    parser.add_argument("- -", help="Test", type=str)
#    parser.add_argument("--background", action="store_true", help="Run the script without GUI")
#    parser.add_argument("--python", action="store_true", help="Run blender with a python file")
#    parser.add_argument("file", help="Path and name of the python file")
   

#    args = parser.parse_args()
#    arguments = vars(args)
#    print(arguments)
   generator = MineGeneration()


# mine = MineGeneration()