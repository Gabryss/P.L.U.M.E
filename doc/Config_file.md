## Overview
The `config.py` script is a configuration module providing essential settings and parameters for a Python project. It defines configuration options and color codes using enumerations, which are likely used across the project for consistency in settings and console outputs.
​
## Imports
- `enum`: For defining enumeration classes.
- `os`: To interact with the operating system, especially for handling file paths.
- `sys`: For interacting with the Python runtime environment.
- `datetime`: For handling date and time, used in default naming.
​

## Config
### General Settings

- `NB_GENERATION`: Number of generations to create.
- `IMAGE_FORMAT`: Format of generated images (e.g., ".png").
- `MESH_FORMAT`: Format of generated 3D meshes (options: 'obj', 'ply', 'usd').
- `OPEN_VISUALIZATION`: Boolean flag to open visualization after generation.
- `GENERATE_MESH`: Boolean flag to generate 3D meshes.
- `SAVE_GRAPH_IMAGE`: Boolean flag to save generated graph images.
- `SAVE_MESH`: Boolean flag to save generated 3D meshes.
- `TYPE_OF_UNDERGROUND`: Type of underground structure ('CAVE' or 'MINE' - MINE not available yet).

### Advanced Settings

- `DEFAULT_MIN_NODES`: Default minimum number of nodes.
- `MAX_CREATED_NODE_ON_CIRCLE`: Maximum number of nodes created on a circle.
- `MAX_RADIUS_NODE`: Maximum radius of a node.
- `DEFAULT_LOOP_CLOSURE_PROBABILITY`: Default probability for loop closure.
- `SELECTED_ALGORITHM`: Selected algorithm for generation ('gaussian_perlin').
- `TEXTURE_SIZE`: Size of textures (options: 16384, 8192, 4096, 1024 pixels).
- `MAX_MESH_TRIANGLES`: Maximum number of triangles in the generated mesh.
- `GPU_ACCELERATION`: Boolean flag for GPU acceleration.

### Gaussian Settings

- `STANDARD_DEVIATION`: Standard deviation for the Gaussian algorithm.

### Perlin Settings

- `MAX_SCALE`: Maximum scale for the Perlin algorithm.
- `MAX_OCTAVES`: Maximum number of octaves for the Perlin algorithm.
- `MAX_PERSISTENCE`: Maximum persistence for the Perlin algorithm.
- `MAX_LACUNARITY`: Maximum lacunarity for the Perlin algorithm.

## Color Enumeration

The `Color` enumeration provides ANSI escape codes for text color formatting. These can be used to enhance console output.

- `HEADER`
- `OKBLUE`
- `OKCYAN`
- `OKGREEN`
- `CVIOLET`
- `WARNING`
- `FAIL`
- `ENDC`
- `BOLD`
- `UNDERLINE`
- `CBLINK`
​
## Usage
These configurations and color codes are likely used across various parts of the project for standardized settings and console output formatting. The `Config` class provides a central place to manage settings, making the code more maintainable and configurable.
​
<!-- --- -->
​
This documentation provides a high-level overview of the `config.py` script. Detailed understanding of each configuration parameter and its impact on the project requires direct reference to the script and its usage within the project's context.