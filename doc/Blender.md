## Prerequisites

- Python
- Blender
- JSON files with specific structure

## Imports

- Built-in Python libraries (`sys`, `os`, `json`, `argparse`)
- Blender Python API (`bpy`)
- Local `config` file

## Classes

### MeshGeneration

This is the main class responsible for generating the mesh. It initializes properties, reads data, creates and modifies the mesh, and exports the final result.

- **Methods:**
    - `__init__(generation_name, index_p)`: Initializes the class and triggers the mesh generation process. Take as input the name of the generation and the iteration index within the generation.
    - `generate_mesh`: The main method that drives the mesh creation process.
    - `initial_cleanup`: Clears default objects from the Blender workspace.
    - `extract_mesh_data`: Reads vertices and edges from the JSON data. Return a list of vertex and edges
    - `load_mesh_in_blender(vertex, edges)`: Creates a new object in Blender using the extracted data. Take a list of vertex and edges as input.
    - `blender_modifiers`: Applies several modifiers to the created object to shape it as required.
    - `flip_normals`: Flips the normals of the object.
    - `export_mesh`: Exports the final mesh to an OBJ file.

## Main Function

This script is designed to be run from the command line and takes several arguments:

- `-index`: Index used for the path (Integer).
- `-name`: Name of the current graph generation (String).
- `--background`: Run the script without GUI.
- `--python`: Run blender with a python file.
- `file`: Path and name of the python file.

These arguments are parsed using the `argparse` library and then used to instantiate the `MeshGeneration` class.

## Execution

On execution, the script creates a 3D mesh object in Blender based on the 2D points read from a JSON file. It then applies specific modifiers to the mesh and exports the final result as an OBJ file.

Please refer to the source code for more details on the implementation.