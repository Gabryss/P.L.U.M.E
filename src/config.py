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

    # General settings
    NB_GENERATION = 1
    IMAGE_FORMAT = ".png"
    OPEN_BLENDER = True
    GENERATE_MESH = True
    SAVE_GRAPH_IMAGE = True
    TYPE_OF_UNDERGROUND = "MINE" # Available: MINE, CAVE

    # Advanced settings
    INITIAL_GRID_SIZE = 10
    DEFAULT_NB_ITERATION = 50
    DEFAULT_MIN_NODES = 1000
    DEFAULT_LOOP_CLOSURE_PROBABILITY = 10
    GPU_ACCELERATION = True 


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