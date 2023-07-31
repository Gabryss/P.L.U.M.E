This Python script is a configuration file for a graph generation algorithm.

## Prerequisites

- Python
- Enum module
- os module
- sys module
- tools module (local)
- datetime module

## Imports

- `Enum`: Python module for creating enumerated constants.
- `os`: Python module for interacting with the operating system.
- `sys`: Python module that provides access to some variables used or maintained by the Python interpreter.
- `tools`: Local module containing various utility functions.
- `datetime`: Python module for manipulating dates and times.

## Classes

### Config

An `Enum` class that provides configuration constants for the graph generation algorithm.

- **Attributes:**
    
    - `PLUME_DIR`: The root directory of the project. (Automatic, do not change)
    - `DEFAULT_NAME`: The default name of the generation, including a timestamp. (Automatic, do not change)
    - `DEFAULT_IMAGE_PATH`: The default path where graph images are stored. (Only used in specific cases)
    - `DEFAULT_NB_GRAPHS`: The default number of graphs to generate.
    - `INITIAL_GRID_SIZE`: The initial size of the grid for graph generation.
    - `DEFAULT_NB_ITERATION`: The default number of iterations for the graph generation algorithm.
    - `DEFAULT_MIN_NODES`: The minimum number of nodes for the graph.
    - `DEFAULT_LOOP_CLOSURE_PROBABILITY`: The probability of loop closure in the graph.
    - `DEFAULT_GUI_DISPLAY`: A boolean flag to indicate whether to display the graph in a GUI (Blender).
    - `DEFAULT_MESH_GENERATION`: A boolean flag to indicate whether to generate a mesh.
    - `SAVE_GRAPH_IMAGE`: A boolean flag to indicate whether to save the generated graph as an image.
    - `IMAGE_FORMAT`: The image format to use when saving the graph image.

The `PLUME_DIR` is added to the Python system path for easy import of modules in the project. All other attributes except `DEFAULT_NAME` are default values that can be overridden in the calling script.

### Color

An `Enum` class that provides console color codes for output formatting.

- **Attributes:**
    
    - `HEADER`
    - `OKBLUE`
    - `OKCYAN`
    - `OKGREEN`
    - `WARNING`
    - `FAIL`
    - `ENDC`
    - `BOLD`
    - `UNDERLINE`

## Execution

This script does not contain a main function and is not intended for standalone execution. Instead, it should be imported into other scripts where the `Config` and `Color` classes can be used to access the configuration constants and color codes.