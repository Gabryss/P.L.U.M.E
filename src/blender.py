import sys
import os
import bpy, bmesh
import json

from bpy import context
from  mathutils import Vector


# Get the path of the PLUME directory
if os.path.dirname(__file__) not in sys.path:
   sys.path.append(os.path.dirname(__file__))

# # Fetch the blender directory
blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

from config import Config, Color



class MeshGeneration:
   def __init__(self, generation_name_p, index_p, graph_path_p) -> None:
      self.generation_name = str(generation_name_p)
      self.index = str(index_p)
      if graph_path_p == "-g":
         self.path = Config.PLUME_DIR.value+"/data/"+self.generation_name+"/"+self.index+"/data.json"
      else:
         self.path = graph_path_p
      self.saved_mesh_path = Config.PLUME_DIR.value+"/data/"+self.generation_name+"/"+self.index+"/mesh."+Config.MESH_FORMAT.value
      self.saved_texture_path = Config.PLUME_DIR.value+"/data/"+self.generation_name+"/"+self.index+"/"
      self.json_file = open(self.path)
      self.data = json.load(self.json_file)
      self.generation_dimension = self.data['generation_dimension']

      self.obj = None
      self.mesh = None
      self.chunks = []
      self.material = None
      self.generate_mesh()


   def generate_mesh(self):
      """
      Main function to create the mesh
      """
      self.initial_cleanup()
      print(f"{Color.BOLD.value}Start graph loading process{Color.ENDC.value}")

      # Extract and load data
      verts, edges = self.extract_mesh_data()
      result_loading = self.load_mesh_in_blender(verts_p=verts, edges_p=edges)
      if result_loading == -1:
         print(f"{Color.FAIL.value}There was a problem while creating the mesh{Color.ENDC.value}")
         exit()
      print(f"{Color.BOLD.value}Graph loading process completed{Color.ENDC.value}")
      
      # Generate geometry and apply modifiers
      self.blender_modifiers()

      # First decimation process (lower the number of polys for better performance)
      if Config.HIGH_POLY.value:
         self.decimate_mesh_polys()
      
      # Slice mesh
      self.slice_mesh()

      # Bake and save and apply the texture
      bpy.ops.object.select_all(action='DESELECT')
      if Config.BAKE_TEXTURE.value:
         for i in range(len(self.chunks)):
            self.chunks[i][1].select_set(True)
            chunck_number = i + 1
            bpy.context.view_layer.objects.active = self.chunks[i][1]
            print(f"{Color.OKBLUE.value}\n ==== Chuck {chunck_number}/{len(self.chunks)} ==== {Color.ENDC.value}")
            self.bake_texture(self.material)
            self.chunks[i][1].select_set(False)
         
         print("\nAll chunks are baked, proceeding to apply the textures\n")
         
         for i in range(len(self.chunks)):
            self.chunks[i][1].select_set(True)
            chunck_number = i + 1
            bpy.context.view_layer.objects.active = self.chunks[i][1]
            self.load_images()
            self.chunks[i][1].select_set(False)

         print("\nAll textures applied for each chunks\n")

      # Final decimation process
      if Config.HIGH_POLY.value and Config.FINAL_DECIMATION.value:
         self.final_decimate_mesh_polys()
      
      bpy.ops.object.select_all(action='SELECT')

      # Export the mesh
      if Config.SAVE_MESH.value:
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
      print("\t-Begin extraction of points")
      verts, edges = [], []
      for i in self.data['nodes']:
         verts.append([
            self.data['nodes'][i]["coordinates"]['x'],
            self.data['nodes'][i]["coordinates"]['y'],
            self.data['nodes'][i]["coordinates"]['z'],
         ])
         for edge in self.data['nodes'][i]['edges']:
            edges.append([
               self.data['nodes'][i]['id'],
               edge
            ])
      print("\t-Extraction done")
      return verts, edges
   

   def load_mesh_in_blender(self, verts_p, edges_p):
      """
      Load the verticies and edges in blender
      """
      print("\t-Load the graph")
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
      print("\t-Graph loaded")
      


   def blender_modifiers(self):
      """
      Create and apply modifiers
      - Skin
      - Subdivision surface
      - Geometry nodes (Including texture creation)
      - Displacement
      """
      print(f"\n{Color.BOLD.value}Start modifiers{Color.ENDC.value}")
      mod_skin = self.obj.modifiers.new('Skin', 'SKIN')
      print("\t-Skin done")

      mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')
      print("\t-Subdivision surface done")
      
      self.geometry_nodes()

      mod_sub_1 = bpy.ops.object.modifier_add(type='SUBSURF')

      mod_displacement = bpy.ops.object.modifier_add(type='DISPLACE')
      bpy.context.object.modifiers["Displace"].strength = 0.05
      bpy.context.object.modifiers["Displace"].texture = self.create_voronoi_texture()
      print("\t-Displacement done")

      # Apply modifiers
      apply_mod = bpy.ops.object.modifier_apply(modifier='Skin') # Create a mesh skin arount the graph
      apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision')
      apply_mod = bpy.ops.object.modifier_apply(modifier='GeometryNodes')
      apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision.001')
      apply_mod = bpy.ops.object.modifier_apply(modifier='Displace')
      print(f"{Color.BOLD.value}Modifiers applied{Color.ENDC.value}")


   def create_voronoi_texture(self):
      """
      Create voronoi texture
      """
      bpy.ops.texture.new()
      bpy.data.textures["Texture"].type = 'CLOUDS'
      bpy.data.textures["Texture"].noise_basis = 'VORONOI_CRACKLE'
      bpy.data.textures["Texture"].noise_type = 'SOFT_NOISE'
      bpy.data.textures["Texture"].noise_scale = 1
      return bpy.data.textures["Texture"]


   def geometry_nodes(self):
      """
      Add geometry nodes
      - Mesh to volume
      - Volume to mesh
      - Mesh to volume second layer
      - Volume to mesh second layer
      - Subdivide mesh
      - Subdivision surface x2
      - Texture noise
      - Value
      - Math x2
      - Vector math
      - Set position
      - Set shade smooth
      - Flip faces
      - Input material
      - Set material
      """
      print(f"{Color.OKGREEN.value}\t-Start geometry node{Color.ENDC.value}")

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
      print("\t\t-Node tree created")

      # Clear default nodes
      for node in node_tree.nodes:
         node_tree.nodes.remove(node)

      # Add a Mesh to Volume node
      mesh_to_volume_node = node_tree.nodes.new(type="GeometryNodeMeshToVolume")
      mesh_to_volume_node.resolution_mode = 'VOXEL_SIZE'
      mesh_to_volume_node.inputs[1].default_value = 10.0   # Density
      mesh_to_volume_node.inputs[2].default_value = 0.2   # Voxel Size
      mesh_to_volume_node.inputs[4].default_value = 0.1   # Interior Band Width
      mesh_to_volume_node.location = (100, 200)
      print("\t\t-Mesh to volume node done")

      # Add a Volume to Mesh node
      volume_to_mesh_node = node_tree.nodes.new(type="GeometryNodeVolumeToMesh")
      volume_to_mesh_node.resolution_mode = 'VOXEL_SIZE'
      volume_to_mesh_node.inputs[1].default_value = 0.2   # Voxel Size
      volume_to_mesh_node.inputs[3].default_value = 0.1   # Threshold
      volume_to_mesh_node.inputs[4].default_value = 0.0   # Adaptivity
      volume_to_mesh_node.location = (400, 200)
      print("\t\t-Volume to mesh node done")

      # Add a Mesh to Volume node
      mesh_to_volume_node_2 = node_tree.nodes.new(type="GeometryNodeMeshToVolume")
      mesh_to_volume_node_2.resolution_mode = 'VOXEL_SIZE'
      mesh_to_volume_node_2.inputs[1].default_value = 5.0   # Density
      mesh_to_volume_node_2.inputs[2].default_value = 0.2   # Voxel Size
      mesh_to_volume_node_2.inputs[4].default_value = 0.1   # Interior Band Width
      mesh_to_volume_node_2.location = (600, 200)
      print("\t\t-Mesh to volume 2 node done")

      # Add a Volume to Mesh node
      volume_to_mesh_node_2 = node_tree.nodes.new(type="GeometryNodeVolumeToMesh")
      volume_to_mesh_node_2.resolution_mode = 'VOXEL_SIZE'
      volume_to_mesh_node_2.inputs[1].default_value = 0.3   # Voxel Size
      volume_to_mesh_node_2.inputs[3].default_value = 0.1   # Threshold
      volume_to_mesh_node_2.inputs[4].default_value = 0.0     # Adaptivity
      volume_to_mesh_node_2.location = (900, 200)
      print("\t\t-Volume to mesh 2 node done")

      if Config.HIGH_POLY.value:
         subdivide_mesh = node_tree.nodes.new(type='GeometryNodeSubdivideMesh')
         subdivide_mesh.location = (1100, 200)
         print("\t\t-Mesh subdivision node done")

         subdivide_surface = node_tree.nodes.new(type='GeometryNodeSubdivisionSurface')
         subdivide_surface.location = (1300, 200)
         subdivide_surface.uv_smooth = 'SMOOTH_ALL'
         print("\t\t-Subdivision surface node done")

      # Noise
      texture_noise = node_tree.nodes.new(type='ShaderNodeTexNoise')
      texture_noise.noise_dimensions = '4D'
      texture_noise.inputs[1].default_value = 2.70 # W
      texture_noise.inputs[2].default_value = 10   # Scale
      texture_noise.inputs[3].default_value = 1    # Detail
      texture_noise.inputs[4].default_value = 1    # Roughness
      texture_noise.inputs[5].default_value = 0.0    # Distortion
      texture_noise.location = (500, -400)
      print("\t\t-Texture noise done")

      value = node_tree.nodes.new(type="ShaderNodeValue")
      value.outputs[0].default_value = 0.1
      value.location = (700, -450)
      print("\t\t-Value node done")

      add = node_tree.nodes.new(type="ShaderNodeMath")
      add.operation = 'ADD'
      add.inputs[1].default_value = 0.5
      add.location = (900, -500)
      print("\t\t-Math 1 node done")

      multiply = node_tree.nodes.new(type="ShaderNodeMath")
      multiply.operation = 'MULTIPLY'
      multiply.use_clamp = True
      multiply.inputs[1].default_value = 1
      multiply.location = (1100, -450)
      print("\t\t-Math 2 node done")

      multiply_add = node_tree.nodes.new(type="ShaderNodeVectorMath")
      multiply_add.operation = 'MULTIPLY_ADD'
      multiply_add.location = (1300, -400)
      print("\t\t-Vector math node done")
      # End noise

      set_position = node_tree.nodes.new(type='GeometryNodeSetPosition')
      set_position.location = (1500, 200)
      print("\t\t-Set position node done")

      subdivide_surface_2 = node_tree.nodes.new(type='GeometryNodeSubdivisionSurface')
      subdivide_surface_2.location = (1700, 200)
      print("\t\t-Subdivision surface 2 node done")


      set_shade_smooth = node_tree.nodes.new(type='GeometryNodeSetShadeSmooth')
      set_shade_smooth.location = (1900, 200)
      print("\t\t-Set shade smooth node done")

      flip_faces = node_tree.nodes.new(type='GeometryNodeFlipFaces')
      flip_faces.location = (2100, 200)
      print("\t\t-Flip faces node done")

      # Material
      material_node = node_tree.nodes.new(type="GeometryNodeInputMaterial")
      material_node.material = self.shader_material()
      material_node.location = (2000, -200)
      print("\t\t-Input material node done")
      # End Material

      set_material = node_tree.nodes.new(type='GeometryNodeSetMaterial')
      set_material.location = (2300, 200)
      print("\t\t-Set material node done")

      # Connect nodes
      node_tree.links.new(mesh_to_volume_node.outputs["Volume"], volume_to_mesh_node.inputs["Volume"])
      node_tree.links.new(volume_to_mesh_node.outputs["Mesh"], mesh_to_volume_node_2.inputs["Mesh"])
      node_tree.links.new(mesh_to_volume_node_2.outputs["Volume"], volume_to_mesh_node_2.inputs["Volume"])
      
      if Config.HIGH_POLY.value:
         node_tree.links.new(volume_to_mesh_node_2.outputs["Mesh"], subdivide_mesh.inputs["Mesh"])
         node_tree.links.new(subdivide_mesh.outputs["Mesh"], subdivide_surface.inputs["Mesh"])
         node_tree.links.new(subdivide_surface.outputs["Mesh"], set_position.inputs["Geometry"])
      
      else:
         node_tree.links.new(volume_to_mesh_node_2.outputs["Mesh"], set_position.inputs["Geometry"])

      
      node_tree.links.new(set_position.outputs["Geometry"], subdivide_surface_2.inputs["Mesh"])
      node_tree.links.new(subdivide_surface_2.outputs["Mesh"], set_shade_smooth.inputs["Geometry"])
      node_tree.links.new(set_shade_smooth.outputs["Geometry"], flip_faces.inputs["Mesh"])
      node_tree.links.new(flip_faces.outputs["Mesh"], set_material.inputs["Geometry"])
      node_tree.links.new(material_node.outputs["Material"], set_material.inputs["Material"])

      # Noise connection
      node_tree.links.new(texture_noise.outputs["Color"], multiply_add.inputs["Vector"])
      node_tree.links.new(multiply_add.outputs["Vector"], set_position.inputs["Offset"])
      node_tree.links.new(value.outputs["Value"], multiply_add.inputs[1])
      node_tree.links.new(value.outputs["Value"], add.inputs["Value"])
      node_tree.links.new(add.outputs["Value"], multiply.inputs["Value"])
      node_tree.links.new(multiply.outputs["Value"], multiply_add.inputs[2])
      print("\t\t-Node links done")

      # Add Group Input and Output nodes for completeness
      node_tree.interface.new_socket(name="Input", in_out='INPUT', socket_type="NodeSocketGeometry")
      node_tree.interface.new_socket(name="Output", in_out='OUTPUT', socket_type="NodeSocketGeometry")



      group_input = node_tree.nodes.new(type="NodeGroupInput")
      # node_tree.outputs.new("NodeSocketGeometry","Geometry")
      group_input.location = (-100, 200)

      group_output = node_tree.nodes.new(type="NodeGroupOutput")
      # node_tree.inputs.new("NodeSocketGeometry","Geometry")
      group_output.location = (2500, 200)

      # Connect the Group Input to Mesh to Volume and Volume to Mesh to Group Output
      node_tree.links.new(group_input.outputs[0], mesh_to_volume_node.inputs["Mesh"])
      node_tree.links.new(set_material.outputs["Geometry"], group_output.inputs[0])
      print("\t\t-Input and output node links done")
      print(f"{Color.OKGREEN.value}\t-Geometry node process completed{Color.ENDC.value}")


   def shader_material(self):
      """
      Proceduraly create rocky texture for the cave
      """
      print(f"{Color.CVIOLET.value}\t\t\t--Create material--{Color.ENDC.value}")
      material = bpy.data.materials.new(name="rock")
      material.use_nodes = True

      principled_bsdf_node = material.node_tree.nodes["Principled BSDF"]
      principled_bsdf_node.inputs["Metallic"].default_value = 0.0
      principled_bsdf_node.inputs["Roughness"].default_value = 0.650
      principled_bsdf_node.location = (2300, 0)


      # First mix
      texture_coordinate_node_1 = material.node_tree.nodes.new(type='ShaderNodeTexCoord')
      texture_coordinate_node_1.location = (450,250)

      mapping_node_1 = material.node_tree.nodes.new(type='ShaderNodeMapping')
      mapping_node_1.location = (650, 250)

      noise_texture_node_1 = material.node_tree.nodes.new(type='ShaderNodeTexNoise')
      noise_texture_node_1.inputs['Scale'].default_value = 80.0
      noise_texture_node_1.inputs['Detail'].default_value = 16.0
      noise_texture_node_1.location = (850, 300)

      noise_texture_node_2 = material.node_tree.nodes.new(type='ShaderNodeTexNoise')
      noise_texture_node_2.inputs['Scale'].default_value = 4.0
      noise_texture_node_2.inputs['Detail'].default_value = 16.0
      noise_texture_node_2.location = (850, 600)

      color_ramp_node_1 = material.node_tree.nodes.new(type='ShaderNodeValToRGB')
      color_ramp_node_1.color_ramp.elements.new(0.632)
      color_ramp_node_1.color_ramp.elements[0].position = 0.429
      color_ramp_node_1.color_ramp.elements[0].color = (0.0563574, 0.0563574, 0.0563574, 1)
      color_ramp_node_1.color_ramp.elements[1].position = 0.555
      color_ramp_node_1.color_ramp.elements[1].color = (0.0846343, 0.104185, 0.115044, 1)
      color_ramp_node_1.color_ramp.elements[2].position = 0.632
      color_ramp_node_1.color_ramp.elements[2].color = (0.173731, 0.1653, 0.159337, 1)
      color_ramp_node_1.location = (1050, 300)

      color_ramp_node_2 = material.node_tree.nodes.new(type='ShaderNodeValToRGB')
      color_ramp_node_2.color_ramp.elements[0].position = 0.429
      color_ramp_node_2.color_ramp.elements[0].color = (0.020863, 0.020863, 0.020863, 1)
      color_ramp_node_2.color_ramp.elements[1].position = 0.632
      color_ramp_node_2.color_ramp.elements[1].color = (0.218045, 0.207349, 0.199787, 1)
      color_ramp_node_2.location = (1050, 600)

      mix_color_node_1 = material.node_tree.nodes.new(type="ShaderNodeMix")
      mix_color_node_1.data_type = 'RGBA'
      mix_color_node_1.blend_type = 'DARKEN'
      mix_color_node_1.inputs['Factor'].default_value = 0.657
      mix_color_node_1.location = (1400, 350)


      # Second mix
      geometry_node = material.node_tree.nodes.new(type='ShaderNodeNewGeometry')
      geometry_node.location = (900,-200)

      color_ramp_node_3 = material.node_tree.nodes.new(type='ShaderNodeValToRGB')
      color_ramp_node_3.color_ramp.elements[0].position = 0.442
      color_ramp_node_3.color_ramp.elements[1].position = 0.534
      color_ramp_node_3.location = (1100, -200)

      mix_color_node_2 = material.node_tree.nodes.new(type="ShaderNodeMix")
      mix_color_node_2.data_type = 'RGBA'
      mix_color_node_2.blend_type = 'MIX'
      mix_color_node_2.inputs[6].default_value = (0,0,0,1)
      mix_color_node_2.location = (1700, 0)


      # Normals
      texture_coordinate_node_2 = material.node_tree.nodes.new(type='ShaderNodeTexCoord')
      texture_coordinate_node_2.location = (900,-600)

      mapping_node_2 = material.node_tree.nodes.new(type='ShaderNodeMapping')
      mapping_node_2.location = (1100, -600)

      noise_texture_node_3 = material.node_tree.nodes.new(type='ShaderNodeTexNoise')
      noise_texture_node_3.inputs['Scale'].default_value = 5.0
      noise_texture_node_3.inputs['Detail'].default_value = 16.0
      noise_texture_node_3.location = (1300, -600)

      bump_node_1 = material.node_tree.nodes.new(type='ShaderNodeBump')
      bump_node_1.location = (1700, -600)

      bump_node_2 = material.node_tree.nodes.new(type='ShaderNodeBump')
      bump_node_2.inputs['Strength'].default_value = 0.1
      bump_node_2.location = (2000, -600)

      #LINKS

      #First Layer
      material.node_tree.links.new(texture_coordinate_node_1.outputs["Object"], mapping_node_1.inputs["Vector"])
      material.node_tree.links.new(mapping_node_1.outputs["Vector"], noise_texture_node_1.inputs["Vector"])
      material.node_tree.links.new(mapping_node_1.outputs["Vector"], noise_texture_node_2.inputs["Vector"])
      material.node_tree.links.new(noise_texture_node_1.outputs["Fac"], color_ramp_node_1.inputs["Fac"])
      material.node_tree.links.new(noise_texture_node_2.outputs["Fac"], color_ramp_node_2.inputs["Fac"])

      material.node_tree.links.new(color_ramp_node_1.outputs["Color"], mix_color_node_1.inputs[6])
      material.node_tree.links.new(color_ramp_node_2.outputs["Color"], mix_color_node_1.inputs[7])

      # Second Layer
      material.node_tree.links.new(geometry_node.outputs["Pointiness"], color_ramp_node_3.inputs["Fac"])
      material.node_tree.links.new(color_ramp_node_3.outputs["Color"], mix_color_node_2.inputs["Factor"])
      material.node_tree.links.new(mix_color_node_1.outputs[2], mix_color_node_2.inputs[7])
      material.node_tree.links.new(mix_color_node_2.outputs[2], principled_bsdf_node.inputs['Base Color'])


      # Normal
      material.node_tree.links.new(texture_coordinate_node_2.outputs["Object"], mapping_node_2.inputs["Vector"])
      material.node_tree.links.new(mapping_node_2.outputs["Vector"], noise_texture_node_3.inputs["Vector"])
      material.node_tree.links.new(noise_texture_node_3.outputs["Fac"], bump_node_1.inputs["Height"])
      material.node_tree.links.new(bump_node_1.outputs["Normal"], bump_node_2.inputs["Normal"])
      material.node_tree.links.new(mix_color_node_2.outputs["Result"], bump_node_2.inputs["Height"])
      material.node_tree.links.new(bump_node_2.outputs["Normal"], principled_bsdf_node.inputs["Normal"])

      self.material = material
      self.principled_bsdf_node = principled_bsdf_node
      print(f"{Color.CVIOLET.value}\t\t\t--Material successfully created--{Color.ENDC.value}")

      return self.material


   def bake_texture(self, material_tree_p):
      """
      Bake and export the texture. Process:
      - Create images for each attribute (Color, Normals, Roughness)
      - Apply smart UV project to create the UV map of the model
      - Use Cycle render and if needed use the GPU acceleration
      - Bake each image
      """
      obj = bpy.context.active_object
      print(f"\n{Color.BOLD.value}Creation of the UV map{Color.ENDC.value}")
      print(f"{Color.CBLINK.value}Can take some time{Color.ENDC.value}")
      obj.select_set(True)
      bpy.context.view_layer.objects.active = obj
      uv_layer = obj.data.uv_layers.new(name="UndergroundUVMap") #new UV layer for underground mapping
      uv_layer.active
      bpy.ops.object.editmode_toggle()
      bpy.ops.mesh.select_all(action='SELECT')
      uv_map = bpy.ops.uv.smart_project()
      print("\t-UV map Done")
      bpy.ops.object.editmode_toggle()
      print(f"{Color.BOLD.value}UV map completed{Color.ENDC.value}")

      print(obj.name)

      print(f"\n{Color.BOLD.value}Start texture baking process{Color.ENDC.value}")
      print(f"{Color.CBLINK.value}Can take some time{Color.ENDC.value}")
      material = material_tree_p
      color_image_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
      color_image = bpy.data.images.new(f'color_rock_{obj.name}', Config.TEXTURE_SIZE.value, Config.TEXTURE_SIZE.value)
      color_image_node.image = color_image

      normal_image_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
      normal_image = bpy.data.images.new(f'normal_rock_{obj.name}', Config.TEXTURE_SIZE.value, Config.TEXTURE_SIZE.value)
      normal_image_node.image = normal_image
      normal_image_node.image.colorspace_settings.name = 'Non-Color'

      roughness_image_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
      roughness_image = bpy.data.images.new(f'roughness_rock_{obj.name}', Config.TEXTURE_SIZE.value, Config.TEXTURE_SIZE.value)
      roughness_image_node.image = roughness_image
      roughness_image_node.image.colorspace_settings.name = 'Non-Color'

      # Set the device_type
      bpy.context.preferences.addons[
         "cycles"
      ].preferences.compute_device_type = "CUDA" # or "OPENCL"
            
      # Set the device and feature set
      bpy.context.scene.render.engine = 'CYCLES'
      if Config.GPU_ACCELERATION.value:
         bpy.context.scene.cycles.device = 'GPU'
      else:
         bpy.context.scene.cycles.device = 'CPU'
      bpy.context.scene.cycles.bake_type = 'DIFFUSE'
      bpy.context.scene.render.bake.use_pass_direct = False
      bpy.context.scene.render.bake.use_pass_indirect = False
      bpy.context.scene.render.bake.target = 'IMAGE_TEXTURES'

      # get_devices() to let Blender detects GPU device
      print(f"\t{Color.UNDERLINE.value}Configuration:{Color.ENDC.value}")
      bpy.context.preferences.addons["cycles"].preferences.get_devices()
      print("\t-",bpy.context.preferences.addons["cycles"].preferences.compute_device_type)
      for d in bpy.context.preferences.addons["cycles"].preferences.devices:
         # d["use"] = 1 # Using all devices, include GPU and CPU
         print("\t -Device: ", d["name"], " Used:", d["use"])
      print("\n")

      #Color image
      print(f"\t{Color.OKCYAN.value}Color texture{Color.ENDC.value}")
      color_image_node.select = True
      material.node_tree.nodes.active = color_image_node
      obj.select_set(True)
      bpy.context.view_layer.objects.active = obj
      bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')
      print("\t-Texture baked")
      color_image.save_render(filepath= self.saved_texture_path + f'color_texture_{obj.name}.png')
      print("\t-Image saved")
      color_image_node.select = False
      print(f"\t{Color.OKCYAN.value}Color texture done{Color.ENDC.value}\n")

      # Normal image
      print(f"\t{Color.OKCYAN.value}Normal texture{Color.ENDC.value}")
      normal_image_node.select = True
      material.node_tree.nodes.active = normal_image_node
      bpy.context.scene.cycles.bake_type = 'NORMAL'
      obj.select_set(True)
      bpy.context.view_layer.objects.active = obj
      bpy.ops.object.bake(type='NORMAL', save_mode='EXTERNAL')
      print("\t-Texture baked")
      normal_image.save_render(filepath= self.saved_texture_path + f'normal_texture_{obj.name}.png')
      print("\t-Image saved")
      normal_image_node.select = False
      print(f"\t{Color.OKCYAN.value}Normal texture done{Color.ENDC.value}\n")


      # Roughness image
      print(f"\t{Color.OKCYAN.value}Roughness texture{Color.ENDC.value}")
      roughness_image_node.select = True
      material.node_tree.nodes.active = roughness_image_node
      bpy.context.scene.cycles.bake_type = 'ROUGHNESS'
      obj.select_set(True)
      bpy.context.view_layer.objects.active = obj
      bpy.ops.object.bake(type='ROUGHNESS', save_mode='EXTERNAL')
      print("\t-Texture baked")
      roughness_image.save_render(filepath= self.saved_texture_path + f'roughness_texture_{obj.name}.png')
      print("\t-Image saved")
      roughness_image_node.select = False
      print(f"\t{Color.OKCYAN.value}Roughness texture done{Color.ENDC.value}\n")

      # Remove the images to save VRAM
      bpy.data.images.remove(color_image)
      bpy.data.images.remove(normal_image)
      bpy.data.images.remove(roughness_image)

      print(f"{Color.BOLD.value}Texture baking process completed{Color.ENDC.value}")


   def load_images(self):
      """
      Load the saved images on the model before export
      """
      # Make sure the right chunk is selected
      obj = bpy.context.active_object
      obj.select_set(True)
      bpy.context.view_layer.objects.active = obj

      # Create new material for the export
      bpy.ops.object.material_slot_remove()
      bpy.ops.object.material_slot_remove()
      material_export = bpy.data.materials.new(name=f"Rock_{obj.name}")
      material_export.use_nodes = True


      principled_bsdf_node = material_export.node_tree.nodes["Principled BSDF"]
      principled_bsdf_node.inputs["Metallic"].default_value = 0.0
      

      color_image_node = material_export.node_tree.nodes.new(type='ShaderNodeTexImage')
      color_image = bpy.data.images.load(self.saved_texture_path + f'color_texture_{obj.name}.png')
      color_image_node.image = color_image


      normal_image_node = material_export.node_tree.nodes.new(type='ShaderNodeTexImage')
      normal_image = bpy.data.images.load(self.saved_texture_path + f'normal_texture_{obj.name}.png')
      normal_image_node.image = normal_image
      normal_image_node.image.colorspace_settings.name = 'Non-Color'

      normal_map_node = material_export.node_tree.nodes.new(type="ShaderNodeNormalMap")



      roughness_image_node = material_export.node_tree.nodes.new(type='ShaderNodeTexImage')
      roughness_image = bpy.data.images.load(self.saved_texture_path + f'roughness_texture_{obj.name}.png')
      roughness_image_node.image = roughness_image
      roughness_image_node.image.colorspace_settings.name = 'Non-Color'



      # Apply materials for the texture
      material_export.node_tree.links.new(color_image_node.outputs['Color'], principled_bsdf_node.inputs['Base Color'])
      material_export.node_tree.links.new(normal_image_node.outputs["Color"], normal_map_node.inputs["Color"])
      material_export.node_tree.links.new(normal_map_node.outputs["Normal"], principled_bsdf_node.inputs["Normal"])
      material_export.node_tree.links.new(roughness_image_node.outputs["Color"], principled_bsdf_node.inputs["Roughness"])

      obj.active_material = bpy.data.materials.get(f"Rock_{obj.name}")

      obj.select_set(False)
      # bpy.ops.file.pack_all()


   def decimate_mesh_polys(self):
      """
      Decimate some polys in the mesh to fit with the max number of polys constraint in the config file
      """
      print(f"\n{Color.BOLD.value}Start mesh decimation process{Color.ENDC.value}")
      print(f"{Color.CBLINK.value}Can take some time{Color.ENDC.value}")
      obj = bpy.context.active_object
      estimated_tri_count = sum([(len(p.vertices) - 2) for p in obj.data.polygons])
      ratio = Config.MAX_MESH_TRIANGLES.value / estimated_tri_count
      print("\t-Generated number of triangles: ", estimated_tri_count)
      print("\t-Desired number of triangles: ", Config.MAX_MESH_TRIANGLES.value)
      print("\t-Ratio: ",ratio)

      if estimated_tri_count > Config.MAX_MESH_TRIANGLES.value:
         decimate_modifier = bpy.ops.object.modifier_add(type='DECIMATE')
         bpy.context.object.modifiers["Decimate"].ratio = ratio
         apply_mod = bpy.ops.object.modifier_apply(modifier='Decimate')

      else:
         print(f"\t{Color.WARNING.value}Mesh not decimated: Number of triangles is less than the max desired number{Color.ENDC.value}")
         return 1
      print(f"{Color.BOLD.value}Mesh decimation process completed{Color.ENDC.value}")

   
   def final_decimate_mesh_polys(self):
      """
      Decimate some polys in the mesh to fit with the max number of polys constraint in the config file
      """
      print(f"\n{Color.BOLD.value}Start final mesh decimation process{Color.ENDC.value}")
      print("This process is used to create even lighter meshes")
      print(f"{Color.CBLINK.value}Can take some time{Color.ENDC.value}")
      obj = bpy.context.active_object
      estimated_tri_count = sum([(len(p.vertices) - 2) for p in obj.data.polygons])
      desired_tri_count = estimated_tri_count * Config.FINAL_DECIMATION_FACTOR.value
      ratio = desired_tri_count / estimated_tri_count
      print("\t-Generated number of triangles: ", estimated_tri_count)
      print("\t-Desired number of triangles: ", desired_tri_count)
      print("\t-Ratio: ",ratio)

      decimate_modifier = bpy.ops.object.modifier_add(type='DECIMATE')
      bpy.context.object.modifiers["Decimate"].ratio = ratio
      apply_mod = bpy.ops.object.modifier_apply(modifier='Decimate')

      print(f"{Color.BOLD.value}Mesh final decimation process completed{Color.ENDC.value}")


   def slice_mesh(self):
      """
      Mesh slicing test
      """
      print(f"\n{Color.BOLD.value}Start slice process{Color.ENDC.value}")

      import math
      # bounding box helper methods
      def bbox(ob):
         return (Vector(b) for b in ob.bound_box)

      # def bbox_center(ob):
      #    return sum(bbox(ob), Vector()) / 8
      def vect_distance(v1,v2):
         return math.sqrt((v1[0]-v2[0])**2+(v1[1]-v2[1])**2+(v1[2]-v2[2])**2)

      def bbox_axes(ob):
         bb = list(bbox(ob))
         return tuple(bb[i] for i in (0, 4, 3, 1))

      def slice(bm, start, end, segments):
         if segments == 1:
            return
         def geom(bm):
            return bm.verts[:] + bm.edges[:] + bm.faces[:]
         planes = [start.lerp(end, f / segments) for f in range(1, segments)]
         
         #p0 = start
         plane_no = (end - start).normalized() 
         while(planes): 
            p0 = planes.pop(0)                 
            ret = bmesh.ops.bisect_plane(bm, 
                     geom=geom(bm),
                     plane_co=p0, 
                     plane_no=plane_no)
            bmesh.ops.split_edges(bm, 
                     edges=[e for e in ret['geom_cut'] 
                     if isinstance(e, bmesh.types.BMEdge)])


      bm = bmesh.new()
      ob = context.object
      me = ob.data
      bm.from_mesh(me)

      o, x, y, z = bbox_axes(ob)
      origin_x = math.dist(o,x)
      origin_y = math.dist(o,y)
      
      if origin_x >= origin_y:
         added_x = int(origin_x // origin_y)
         added_y = 1


      if origin_x < origin_y:
         added_y = int(origin_y // origin_y)
         added_x = 1
      
      x_segments = added_x * Config.NUMBER_OF_CHUNKS.value
      y_segments = added_y * Config.NUMBER_OF_CHUNKS.value
      
      if self.generation_dimension == "3D":
         z_segments = Config.NUMBER_OF_CHUNKS.value
      else:
         z_segments = 1

      slice(bm, o, x, x_segments)
      slice(bm, o, y, y_segments)
      slice(bm, o, z, z_segments)
      bm.to_mesh(me)

      bpy.ops.object.mode_set(mode='EDIT')
      bpy.ops.mesh.separate(type='LOOSE')
      bpy.ops.object.mode_set()
      self.chunks = bpy.context.scene.objects.items()


      print(f"\t-Slicing done, {len(self.chunks)} chunks created")     
      print(f"{Color.BOLD.value}Slice process completed{Color.ENDC.value}")



   def export_mesh(self):
      """
      Export the mesh in the desired format
      """
      print(f"\n{Color.BOLD.value}Begin mesh export process{Color.ENDC.value}")
      bpy.data.objects['Underground'].select_set(True)

      mesh_obj = bpy.context.active_object

      mesh_obj.data.materials.append(self.material)

      # Make sure the directory exist
      if not os.path.exists(os.path.dirname(self.saved_mesh_path)):
            os.makedirs(os.path.dirname(self.saved_mesh_path))

      # Export the mesh
      if Config.MESH_FORMAT.value == 'obj':
         bpy.ops.wm.obj_export(filepath=self.saved_mesh_path,
                               export_selected_objects=True)
      
      elif Config.MESH_FORMAT.value == 'usd':
         bpy.ops.wm.usd_export(filepath=self.saved_mesh_path)
      
      elif Config.MESH_FORMAT.value == 'ply':
         bpy.ops.export_mesh.ply(filepath=self.saved_mesh_path)
      
      elif Config.MESH_FORMAT.value == 'fbx':
         bpy.ops.export_scene.fbx(filepath=self.saved_mesh_path, use_selection=True)
      
      else:
         print(f"\t{Color.FAIL.value}-Problem with the export, wrong format{Color.ENDC.value}")
         return -1
      
      print("\t-Export done")      
      print(f"{Color.BOLD.value}Mesh successfully exported{Color.ENDC.value}")



if __name__ == '__main__':
   generator = MeshGeneration(index_p=sys.argv[-3],
                              generation_name_p= sys.argv[-1],
                              graph_path_p=sys.argv[-5])