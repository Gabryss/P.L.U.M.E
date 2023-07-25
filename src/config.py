from enum import Enum
import os
import sys
import bpy
import glob
from tools import Tools

class Config(Enum):
    PLUME_DIR = os.path.dirname(os.path.dirname(__file__))

    # Append the PLUME path to the python path:
    if PLUME_DIR not in sys.path:
        sys.path.append(PLUME_DIR)

    DEFAULT_CSV_PATH = PLUME_DIR + "/data/raw_data/grid_data.csv"
    DEFAULT_GRAPH_PATH = PLUME_DIR +"/data/raw_data/data.json"

    DEFAULT_GRID_SIZE = 3
    DEFAULT_NB_ITERATION = 50
    DEFAULT_GRID_PATH = "data/images/graph_0"
    DEFAULT_MIN_NODES = 500
    DEFAULT_LOOP_CLOSURE_PROBABILITY = 70
    DEFAULT_GUI_DISPLAY = True
    DEFAULT_GENERATE_PNG = False
    DEFAULT_BLENDER_PATH = Tools.find_file("blender")




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