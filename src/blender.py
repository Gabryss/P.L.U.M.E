import sys
import os
import bpy
import json

# Fetch the blender directory
blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

print(blend_dir)
# Open the data file
json_file = open('/home/gabriel/Documents/PhD/Lava_tubes/python/P.L.U.M.E/data/raw_data/data.json')

# Load the data into a variable
data = json.load(json_file)

def initial_cleanup():
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

def load_mesh_data(data_p):
   """
   Load graph data into python variables
   """
   verts, edges = [], []
   for i in data:
      verts.append([
         data[i]["coordinates"]['x'],
         data[i]["coordinates"]['y'],
         0.0
      ])
      for child in data[i]['children']:
         edges.append([
            data[i]['id']-1,
            child-1
         ])
      
      # print(data[i])
      # print(data[i]["coordinates"])
   print("Verts :", verts," \nEdges :", edges)
   
   return verts, edges


initial_cleanup()
verts, edges = load_mesh_data(data_p=data)


mesh = bpy.data.meshes.new('Underground')
obj = bpy.data.objects.new('Underground', mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

mesh.from_pydata(verts, edges, [])

# Create modifiers
mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')
mod_skin = obj.modifiers.new('Skin', 'SKIN')
mod_sub = bpy.ops.object.modifier_add(type='SUBSURF')

# Apply modifiers
# apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision')
# apply_mod = bpy.ops.object.modifier_apply(modifier='Skin') # Create a mesh skin arount the graph
# apply_mod = bpy.ops.object.modifier_apply(modifier='Subdivision.001')


# Flip the normals
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.select_all(action='SELECT') # Select all faces
bpy.ops.mesh.flip_normals() # just flip normals


# Export the mesh
blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
target_file = os.path.join(directory, 'myfile.obj')
print(target_file)
bpy.data.objects['Underground'].select_set(True)

bpy.ops.wm.obj_export(filepath='data/mesh_files/test.obj',
                      export_selected_objects=True)

json_file.close()