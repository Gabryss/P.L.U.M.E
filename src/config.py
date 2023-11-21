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
    MESH_FORMAT = 'obj'        # Available: obj, ply
    OPEN_VISUALIZATION = True
    GENERATE_MESH = True
    SAVE_GRAPH_IMAGE = False
    SAVE_MESH = True
    TYPE_OF_UNDERGROUND = "MINE" # Available: MINE, CAVE #Not available yet

    # ==== Advanced settings ====
    DEFAULT_MIN_NODES = 100
    MAX_CREATED_NODE_ON_CIRCLE = 2
    MAX_RADIUS_NODE = 5.0
    DEFAULT_LOOP_CLOSURE_PROBABILITY = 10
    SELECTED_ALGORITHM = "gaussian_perlin" # Available: gaussian_perlin
    TEXTURE_SIZE = 4096      # 16384, 8192, 4096, 1024 pixels
    MAX_MESH_TRIANGLES = 1000000 # 1Million triangles: 1000000
    GPU_ACCELERATION = True 


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
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'