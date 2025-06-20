from enum import Enum
import os
import sys
import datetime

class Config(Enum):
    PLUME_DIR = os.path.dirname(os.path.dirname(__file__))
    DEFAULT_NAME = "Generation_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # Append the PLUME path to the python path:
    if PLUME_DIR not in sys.path:
        sys.path.append(PLUME_DIR)  

    # ==== General settings ====
    # ==========================
    NB_GENERATION = 1
    GENERATION_SIZE = (500,100,100)            # Size of the generated environment
    
    #Graph image
    IMAGE_FORMAT = ".png"
    GENERATE_GRAPH_IMAGE = True
    SAVE_GRAPH_IMAGE = True
    THEME = "white"                         # Light or dark mode. Available: white, dark

    #Mesh
    OPEN_VISUALIZATION = False               # Only open the last generation on sequential generation
    MESH_FORMAT = 'usd'                     # Available: obj, ply(no textures), usd, fbx    
    GENERATE_MESH = True                    # Use blender to generate the mesh
    SAVE_MESH = True                       # Save the mesh in data folder
    BAKE_TEXTURE = False                    # Create, bake and save the textures (Color, Normal and Roughness maps)
    TYPE_OF_UNDERGROUND = "CAVE"            # Available: MINE (#Not available yet), CAVE

    # ==== Advanced settings ====
    # ===========================
    NB_NODES = 250                          # Number of nodes in the generation
    MAX_CREATED_NODE_ON_CIRCLE = 2          # Maximal number of nodes created per nodes
    MAX_RADIUS_NODE = 7.0                   # Distance between the nodes
    DEFAULT_LOOP_CLOSURE_PROBABILITY = 10   # Probability of connecting two close nodes
    SELECTED_ALGORITHM = "gaussian_perlin"  # Available: gaussian_perlin, mine
    TEXTURE_SIZE = 1024                     # 32768(Don't try this), 16384 (64GB RAM or more is needed), 8192 (32GB RAM or more is needed), 4096, 1024 pixels
    MAX_MESH_TRIANGLES = 1000000            # 1Million triangles: 1000000 (Upper threshold for vscode obj visualizer)
    FINAL_DECIMATION = False
    FINAL_DECIMATION_FACTOR = 0.8           # Percentage of final mesh decimation (after texture baking). 0.8 means keep 80% of the polys number of the model
    GPU_ACCELERATION = True                 # Use the GPU instead of the GPU (Spead up the texture baking)
    PARALLELIZATION = False                 # If true the prompt in the terminal might be inconsistent
    HIGH_POLY = False                       # If false, the generation is significantly faster
    THREE_DIMENSION_GENERATION = True
    SLICE_MESH = False
    NUMBER_OF_CHUNKS = 3

    #Gaussian
    MEAN = 0.0
    STANDARD_DEVIATION = 0.5

    Z_AXIS_GAUSSIAN_MEAN = 0.0                      #Shift the Z axis by this value
    Z_AXIS_GAUSSIAN_STANDARD_DEVIATION = 0.1        #Higher value here leads to more extremums
    Z_AXIS_LAYER_PROB = 10                          #Percentage of one node to "step down". 10 means 10%
    Z_AXIS_LAYER_STEP = 4                           #Distance of one step between layers
    Z_AXIS_STEP_DOWN_XY_SHIFT = 1.2

    # Perlin
    MAX_SCALE = 10.0
    MAX_OCTAVES = 1.0
    MAX_PERSISTENCE = 5.0
    MAX_LACUNARITY = 2.0


class Color(Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    CVIOLET = '\33[35m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CBLINK    = '\33[5m'
