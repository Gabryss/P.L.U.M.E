# P.L.U.M.E

Procedural Lava-Tube Underground Modeling Engine: A generator that uses procedural generation techniques and graph algorithms to create detailed and visually appealing lava tube structures.



## Algorithms
The generator use a selected algorithm to create the graph shape. Then once the underground skeleton is created using graph, the Blender API is required to create the mesh around it. The benefit of this method would first be the large number of generated mesh that could be created within a minute. Then the resulted mesh highly depends on the used algorithm and given parameters so the generator is thoroughly tunable.

### Probabilistic
robability plays an integral role in the generation of random graphs. Here are some key ways it contributes:

Node Connection Probability: As mentioned in the Erdős-Rényi model, for every pair of nodes, an edge is created based on a specified probability. This randomness influences the structure of the generated graph, making it different each time it is generated.

Weight Assignment: In weighted graphs, probability can dictate the weight (or cost) assigned to the edges. For instance, a random number from a given distribution can be assigned as the weight of an edge. In our case it will only be a Poisson distributon (0 or 1).

Type of Distribution: The distribution type selected for generating the probability can heavily influence the graph's characteristics. For instance, in preferential attachment models (like the Barabási-Albert model), the probability that a new edge has one endpoint at a node (existing in the graph) is proportional to the node's degree. This creates a "rich-get-richer" effect, resulting in a scale-free network that has nodes (called hubs) with a degree much larger than the average.

Choosing the Type of Graph: The graph's nature (directed, undirected, weighted, unweighted) can also be determined probabilistically. This choice will, in turn, influence the way the graph is generated and structured.

Determining Node and Edge Attributes: Probability can be used to randomly assign attributes to nodes and edges. These attributes could represent various properties of the node/edge in the modeled system, and the randomness could represent the inherent variability in those properties in the real world.

Control the Density of the Graph: The probability can control the number of edges in the graph, and hence, the density or sparseness of the graph. A higher probability will lead to a denser graph with more edges, and a lower probability will generate a sparser graph.

In all these ways, probability provides a way to introduce randomness and variability into graph generation, helping to create more realistic and varied models of complex systems.


### Voronoi
The Voronoi tessellations (or Dirichlet tessellations) is an algorithm.

More informations [here](https://hpaulkeeler.com/voronoi-dirichlet-tessellations/)

Voronoi tessellation is a mathematical concept named after Georgy Voronoi, a Russian mathematician. It is also referred to as Voronoi diagram, Voronoi partition, or Voronoi decomposition.

In the simplest terms, a Voronoi tessellation of a plane with a set of distinct points is a partitioning of that plane into regions. Each region corresponds to a specific point and contains all locations in the plane that are closer to this point than to any other.

Here is a step-by-step process of how it's constructed:

- Start with a set of points on a plane, known as "seed" points.
- For each seed point, construct a region consisting of all the points that are closer to this seed than to any other. This is done by drawing boundaries which are equidistant between pairs of seed points.
- The end result is a mosaic of polygons, each associated with one seed point and containing all the points closer to that seed point than to any other. These polygons are called Voronoi cells.

Voronoi tessellations are used in a variety of field but could be used to generate graphs that are not based on a perfect grid shape. In our case it break the "grid-like" shape generation used for our algorithm.


### Fibonacci Lattice
Fibonacci Lattice, also known as Fibonacci grid or Fibonacci spiral, is a geometric distribution of points in a disk, placing points in a very regular but non-uniform manner. It is frequently used in computer graphics and computational geometry due to its properties.

In the context of organic graph generation, the Fibonacci Lattice could be used to create irregularity. Since the points in the Fibonacci Lattice are distributed in a non-uniform way, the graph nodes derived from these points will also be non-uniform. This introduces some irregularity and randomness in the graph, contributing to its 'organic' feel. Additionally, the Fibonacci Lattice can be used for the point distribution generation. It can generate the vertices of a graph, placing them in a way that fills a certain area while maintaining a certain level of distance from each other. This is useful in creating an organic structure as it avoids an overly uniform or random distribution of nodes, instead providing a more natural feel.

## Metric distorsion
Once generated, the graph could be distorted to create a more realistic and organic shape.

In our context, metric distortion, also referred to as distortion or stretch, is a measure of how much a function (typically a mapping or embedding) distorts the distances between points. Instead of having straight lines of defined length, metric distortion could introduce more randomness into the size of our tunnels.

## Mesh creation
During this project, I decided to use Blender API to create the mesh based on a graph skeleton. Blender has a wide community that allows extensive support as well as all the default tools to achieve mesh generation.

## Setup
### Requirements
- Python >= 3.8
- numpy >= 1.21.4
- pyglet >= 1.5.21

### Install the libraries
Before launching the generation, the library installation is required. To achieve it, it is first recommended to install a Python virtual environment. At the root directory of the PLUME project use this command:

```python
/P.L.U.M.E$ python3 -m venv venv
```

Once the virtual environment directory created please activate it:

```python
/P.L.U.M.E$ source venv/bin/activate
```

You should now have `(venv)` at the beggining of your termial line.
Execute this line:

```python
pip install -r requirements.txt
```
Once the installation is completed. Your environment should now be ready.


### Launch the generator
To initiate procedural generation, run the `generation.py` file using pyglet version 1.5.21 or higher. It's important to note that this generator is not compatible with Python 2.x.

```python
$ python3 src/generation.py
```

It is also possible to add specific arguments to the command line:
- \-h Open help
- \-s <int> Specify grid size
- \-nb_g <int> Number of generated graph
- \-name <name> Name of the current graph generation (Time and date will be automatically added to it). No space allowed.

Example:
```python
$ python3 src/generation.py -s 4 -nb_g 10 -name Chanel
```

## Results

<p align="center">
    <img width="500" height="400" src="doc/images/graph_first_loop.png">
    <div align="center">First loop generation</div>
</p>



<p align="center">
    <img width="500" height="400" src="doc/images/2d_flat_grid_generation.png">
    <div align="center">Flat generation using 2D grid</div>
</p>