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

from config import Config, Color

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
      result_loading = self.load_mesh_in_blender(verts_p=verts, edges_p=edges)
      if result_loading == -1:
         print(f"{Color.FAIL.value}There was a problem while creating the mesh{Color.ENDC.value}")
         exit()
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
         for edge in self.data[i]['edges']:
            edges.append([
               self.data[i]['id']-1,
               edge-1
            ])         
      return verts, edges
   

   def load_mesh_in_blender(self, verts_p, edges_p):
      """
      Load the verticies and edges in blender
      """
      verts = verts_p
      edges = edges_p
      self.mesh = bpy.data.meshes.new('Underground')
      self.obj = bpy.data.objects.new('Underground', self.mesh)
      col = bpy.data.collections.get("Collection")
      col.objects.link(self.obj)
      bpy.context.view_layer.objects.active = self.obj

      self.mesh.from_pydata(verts, edges, [])
      if not self.mesh:
         return -1


   def blender_modifiers(self):
      """
      Create and apply modifiers
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
   parser.add_argument("--background", action="store_true", help="Run the script without GUI")
   parser.add_argument("--python", action="store_true", help="Run blender with a python file")
   parser.add_argument("file", help="Path and name of the python file")
   

   args = parser.parse_args()
   arguments = vars(args)
   generator = MeshGeneration(index_p=arguments['index'],
                              generation_name_p=arguments['name'])