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
    NB_GENERATION = 1
    IMAGE_FORMAT = ".png"
    MESH_FORMAT = 'obj'                     # Available: obj, ply(no textures), usd, fbx
    OPEN_VISUALIZATION = True               # Only open the last generation on sequential generation
    GENERATE_MESH = True
    SAVE_GRAPH_IMAGE = True
    SAVE_MESH = True
    TYPE_OF_UNDERGROUND = "CAVE"            # Available: MINE (#Not available yet), CAVE

    # ==== Advanced settings ====
    DEFAULT_MIN_NODES = 100
    MAX_CREATED_NODE_ON_CIRCLE = 2
    MAX_RADIUS_NODE = 5.0
    DEFAULT_LOOP_CLOSURE_PROBABILITY = 10
    SELECTED_ALGORITHM = "gaussian_perlin"  # Available: gaussian_perlin
    TEXTURE_SIZE = 8192                     # 32768(Don't try this), 16384 (64GB RAM or more is needed), 8192 (32GB RAM or more is needed), 4096, 1024 pixels
    MAX_MESH_TRIANGLES = 1000000            # 1Million triangles: 1000000 (Upper threshold for vscode obj visualizer)
    GPU_ACCELERATION = True                 # Use the GPU instead of the GPU (Spead up the texture baking)
    PARALLELIZATION = False                 # If true the prompt in the terminal might be inconsistent
    HIGH_POLY = False                       # If false, the generation is significantly faster
    


    #Gaussian
    STANDARD_DEVIATION = 0.1

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