import sys
import os
import bpy
import json
import argparse

# Get the path of the PLUME directory
if os.path.dirname(__file__) not in sys.path:
   sys.path.append(os.path.dirname(__file__))

# # Fetch the blender directory
blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

from config import Config

class MeshGeneration:
   def __init__(self, generation_name_p, index_p) -> None:
      self.generation_name = str(generation_name_p)
      self.index = str(index_p)
      self.path = Config.PLUME_DIR.value+"/data/raw_data/"+self.generation_name+"/"+self.index+"/data.json"
      self.saved_mesh_path = Config.PLUME_DIR.value+"/data/mesh_files/"+self.generation_name+"/"+self.index+"/mesh.obj"
      self.json_file = open(self.path)
      self.data = json.load(self.json_file)
      self.obj = None
      self.mesh = None
      self.generate_mesh()
      exit()


   def generate_mesh(self):
      """
      Main function to create the mesh
      """
      self.initial_cleanup()
      verts, edges = self.extract_mesh_data()
      self.load_mesh_in_blender(verts_p=verts, edges_p=edges)
      self.blender_modifiers()
      self.flip_normals()
      self.export_mesh()
      self.json_file.close()


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
      Load graph data into python variables
      """
      verts, edges = [], []
      for i in self.data:
         verts.append([
            self.data[i]["coordinates"]['x'],
            self.data[i]["coordinates"]['y'],
            0.0
         ])
         for child in self.data[i]['children']:
            edges.append([
               self.data[i]['id']-1,
               child-1
            ])
         
         # print(data[i])
         # print(data[i]["coordinates"])
      print("Verts :", verts," \nEdges :", edges)
      return verts, edges
   

   def load_mesh_in_blender(self, verts_p, edges_p):
      """
      """
      verts = verts_p
      edges = edges_p
      self.mesh = bpy.data.meshes.new('Underground')
      self.obj = bpy.data.objects.new('Underground', self.mesh)
      col = bpy.data.collections.get("Collection")
      col.objects.link(self.obj)
      bpy.context.view_layer.objects.active = self.obj

      self.mesh.from_pydata(verts, edges, [])


   def blender_modifiers(self):
      """
      """
      mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')
      mod_skin = self.obj.modifiers.new('Skin', 'SKIN')
      mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')

      # Apply modifiers
      apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision')
      apply_mod = bpy.ops.object.modifier_apply(modifier='Skin') # Create a mesh skin arount the graph
      apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision.001')


   def flip_normals(self):
      """
      Flip the normals
      """
      bpy.ops.object.editmode_toggle()
      bpy.ops.mesh.select_all(action='SELECT') # Select all faces
      bpy.ops.mesh.flip_normals() # just flip normals


   def export_mesh(self):
      """
      Export the mesh in the desired format
      """
      blend_file_path = bpy.data.filepath
      directory = os.path.dirname(blend_file_path)
      target_file = os.path.join(directory, 'myfile.obj')
      print(target_file)
      bpy.data.objects['Underground'].select_set(True)

      # Make sure the directory exist
      if not os.path.exists(os.path.dirname(self.saved_mesh_path)):
            os.makedirs(os.path.dirname(self.saved_mesh_path))

      # Export the mesh
      bpy.ops.wm.obj_export(filepath=self.saved_mesh_path,
                            export_selected_objects=True)


if __name__ == '__main__':
   parser = argparse.ArgumentParser(
                                description="PLUME project. Mesh generation based on a json file that provide data as x,y,z coordinates. Then based on the created structure, apply a circular skin around it to create the edges of the underground mesh.",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
   parser.add_argument("-index", help="Index used for the path", type=int)
   parser.add_argument("-name", help="Name of the current graph generation", type=str)
   parser.add_argument("--background", action="store_true", help="Name of the current graph generation")
   parser.add_argument("--python", action="store_true", help="Name of the current graph generation")
   parser.add_argument("file", help="Name of the current graph generation")
   

   args = parser.parse_args()
   arguments = vars(args)
   generator = MeshGeneration(index_p=arguments['index'],
                              generation_name_p=arguments['name'])






# # Open the data file
# json_file = open(f'{Config.PLUME_DIR.value}/data/raw_data/data.json')

# # Load the data into a variable
# data = json.load(json_file)

# def initial_cleanup():
#    """
#    Remove the default object of Blender
#    """
#    bpy.ops.object.select_all(action='DESELECT')
#    bpy.data.objects['Cube'].select_set(True)
#    bpy.ops.object.delete()
#    bpy.data.objects['Camera'].select_set(True)
#    bpy.ops.object.delete()
#    bpy.data.objects['Light'].select_set(True)
#    bpy.ops.object.delete()

# def load_mesh_data(data_p):
#    """
#    Load graph data into python variables
#    """
#    verts, edges = [], []
#    for i in data:
#       verts.append([
#          data[i]["coordinates"]['x'],
#          data[i]["coordinates"]['y'],
#          0.0
#       ])
#       for child in data[i]['children']:
#          edges.append([
#             data[i]['id']-1,
#             child-1
#          ])
      
#       # print(data[i])
#       # print(data[i]["coordinates"])
#    print("Verts :", verts," \nEdges :", edges)
   
#    return verts, edges


# initial_cleanup()
# verts, edges = load_mesh_data(data_p=data)


# mesh = bpy.data.meshes.new('Underground')
# obj = bpy.data.objects.new('Underground', mesh)
# col = bpy.data.collections.get("Collection")
# col.objects.link(obj)
# bpy.context.view_layer.objects.active = obj

# mesh.from_pydata(verts, edges, [])

# # Create modifiers
# mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')
# mod_skin = obj.modifiers.new('Skin', 'SKIN')
# mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')

# # Apply modifiers
# # apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision')
# # apply_mod = bpy.ops.object.modifier_apply(modifier='Skin') # Create a mesh skin arount the graph
# # apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision.001')


# # Flip the normals
# bpy.ops.object.editmode_toggle()
# bpy.ops.mesh.select_all(action='SELECT') # Select all faces
# bpy.ops.mesh.flip_normals() # just flip normals


# # Export the mesh
# blend_file_path = bpy.data.filepath
# directory = os.path.dirname(blend_file_path)
# target_file = os.path.join(directory, 'myfile.obj')
# print(target_file)
# bpy.data.objects['Underground'].select_set(True)

# bpy.ops.wm.obj_export(filepath='data/mesh_files/test.obj',
#                       export_selected_objects=True)

# json_file.close()