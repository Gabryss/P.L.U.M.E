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

    # Select an algorithm
    # -gaussian_perlin
    SELECTED_ALGORITHM = "gaussian_perlin"

    # Integers
    DEFAULT_NB_GRAPHS = 1
    DEFAULT_NB_ITERATION = 50

    DEFAULT_MIN_NODES = 100
    DEFAULT_LOOP_CLOSURE_PROBABILITY = 10
    
    # Booleans
    DEFAULT_GUI_DISPLAY = False
    DEFAULT_MESH_GENERATION = False
    SAVE_GRAPH_IMAGE = True
    IMAGE_FORMAT = ".png"


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