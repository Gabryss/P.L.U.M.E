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
      print("EXTRACT DONE")
      result_loading = self.load_mesh_in_blender(verts_p=verts, edges_p=edges)
      if result_loading == -1:
         print(f"{Color.FAIL.value}There was a problem while creating the mesh{Color.ENDC.value}")
         exit()
      print("LOAD MESH DONE")
      self.blender_modifiers()
      print("MODIFIER DONE")
      self.flip_normals()
      print("FLIP NORMALS DONE")
      self.export_mesh()
      self.json_file.close()
      print("EXPORT MESH DONE")


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
               self.data[i]['id'],
               edge
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
      # mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')
      # print("SUBSURF DONE")
      
      mod_skin = self.obj.modifiers.new('Skin', 'SKIN')
      print("SKIN DONE")

      mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')
      print("SUBSURF DONE")
      
      # self.geometry_nodes()

      # mod_sub_1 = bpy.ops.object.modifier_add(type='SUBSURF')

      # Apply modifiers
      apply_mod = bpy.ops.object.modifier_apply(modifier='Skin') # Create a mesh skin arount the graph
      apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision')
      # apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision001')


   def geometry_nodes(self):
      """
      Add geometry nodes
      - Mesh to volume
      - Volume to mesh
      """

      # Add a Geometry Nodes modifier to the object
      geom_modifier = self.obj.modifiers.new(name="GeometryNodes", type='NODES')

      # Create a new Geometry Nodes tree
      node_tree_name = "UndergroundTree"
      if not bpy.data.node_groups.get(node_tree_name):
         node_tree = bpy.data.node_groups.new(name=node_tree_name, type='GeometryNodeTree')
      else:
         node_tree = bpy.data.node_groups[node_tree_name]

      # Link the tree to the modifier
      geom_modifier.node_group = node_tree

      # Clear default nodes
      for node in node_tree.nodes:
         node_tree.nodes.remove(node)

      # Add a Mesh to Volume node
      mesh_to_volume_node = node_tree.nodes.new(type="GeometryNodeMeshToVolume")
      mesh_to_volume_node.location = (100, 200)

      # Add a Volume to Mesh node
      volume_to_mesh_node = node_tree.nodes.new(type="GeometryNodeVolumeToMesh")
      volume_to_mesh_node.location = (300, 200)

      # Connect nodes
      node_tree.links.new(mesh_to_volume_node.outputs["Volume"], volume_to_mesh_node.inputs["Volume"])

      # Add Group Input and Output nodes for completeness
      group_input = node_tree.nodes.new(type="NodeGroupInput")
      node_tree.outputs.new("NodeSocketGeometry","Geometry")
      group_input.location = (-100, 200)
      group_output = node_tree.nodes.new(type="NodeGroupOutput")
      node_tree.inputs.new("NodeSocketGeometry","Geometry")
      group_output.location = (500, 200)

      # Connect the Group Input to Mesh to Volume and Volume to Mesh to Group Output
      node_tree.links.new(group_input.outputs["Geometry"], mesh_to_volume_node.inputs["Mesh"])
      node_tree.links.new(volume_to_mesh_node.outputs["Mesh"], group_output.inputs["Geometry"])


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