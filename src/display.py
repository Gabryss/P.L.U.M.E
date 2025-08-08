# SPDX-License-Identifier: BSD-3-Clause

"""
Display a graph using Pyvista library
"""
import json
from tqdm import tqdm
from config import Config
import numpy as np
import pyvista as pv
import math

class Display():
    def __init__(self, data_path, voxel_size=0.6, node_radius=1.0, edge_radius=1.0, smoothing=True, n_iter=50, relaxation_factor=0.1):
        self.data_path = data_path + "/data.json"
        self.voxel_size = voxel_size
        self.node_radius = node_radius
        self.edge_radius = edge_radius
        self.smoothing = smoothing
        self.n_iter = n_iter
        self.relaxation_factor = relaxation_factor

        self.positions = None
        self.radii = None
        self.edges = None
        self.vol_shape = None
        self.grid = None
        self.contours = None

    def load_graph(self):
        with open(self.data_path) as f:
            data = json.load(f)
        nodes = data['nodes']

        self.positions = np.array([[v['coordinates']['x'], v['coordinates']['y'], v['coordinates']['z']] for v in nodes.values()])
        self.radii = np.array([self.node_radius for _ in nodes.values()])
        edges = []
        for nid, node in nodes.items():
            nid = int(nid)
            for nb in node['edges']:
                if (nid, nb) not in edges and (nb, nid) not in edges:
                    edges.append((nid, nb))
        self.edges = edges

    def voxelize(self):
        margin = 2 * max(self.node_radius, self.edge_radius)
        mins = self.positions.min(axis=0) - margin
        maxs = self.positions.max(axis=0) + margin

        xs = np.arange(mins[0], maxs[0], self.voxel_size)
        ys = np.arange(mins[1], maxs[1], self.voxel_size)
        zs = np.arange(mins[2], maxs[2], self.voxel_size)
        X, Y, Z = np.meshgrid(xs, ys, zs, indexing='ij')
        grid_points = np.stack([X, Y, Z], axis=-1).reshape(-1, 3)

        voxels = np.zeros(len(grid_points), dtype=bool)

        # Voxelize nodes as spheres
        for pos in self.positions:
            dists = np.linalg.norm(grid_points - pos, axis=1)
            voxels |= dists <= self.node_radius

        # Voxelize edges as cylinders/tubes
        def point_to_segment_dist(p, a, b):
            ap = p - a
            ab = b - a
            ab_dot = np.dot(ab, ab)
            if ab_dot == 0:
                return np.linalg.norm(ap)
            t = np.clip(np.dot(ap, ab) / ab_dot, 0, 1)
            closest = a + t * ab
            return np.linalg.norm(p - closest)

        # for i1, i2 in self.edges:
        for i1, i2 in tqdm(self.edges, desc="\t\t\tProgress"):
        
            a = self.positions[i1]
            b = self.positions[i2]
            rad = self.edge_radius
            seg_min = np.minimum(a, b) - rad
            seg_max = np.maximum(a, b) + rad
            mask = np.all((grid_points >= seg_min) & (grid_points <= seg_max), axis=1)
            points_in_box = grid_points[mask]
            if len(points_in_box) == 0:
                continue
            dists = np.array([point_to_segment_dist(p, a, b) for p in points_in_box])
            inside = dists <= rad
            voxels[mask] |= inside

        vol_shape = (len(xs), len(ys), len(zs))
        self.vol_shape = vol_shape
        vol = voxels.reshape(vol_shape)

        # Pad for isosurface extraction
        vol_points = np.pad(vol, ((0,1), (0,1), (0,1)), mode='constant', constant_values=0)
        self.grid_origin = (xs[0], ys[0], zs[0])
        self.grid_spacing = (self.voxel_size, self.voxel_size, self.voxel_size)
        self.grid_dims = vol_points.shape

        # Create ImageData for PyVista
        grid = pv.ImageData()
        grid.dimensions = vol_points.shape
        grid.origin = self.grid_origin
        grid.spacing = self.grid_spacing
        grid.point_data['cave'] = vol_points.flatten(order='F')
        self.grid = grid

    def extract_surface(self):
        contours = self.grid.contour(isosurfaces=[0.5], scalars="cave")
        if self.smoothing:
            contours = contours.smooth(n_iter=self.n_iter, relaxation_factor=self.relaxation_factor)
        self.contours = contours

    def plot(self):
        pl = pv.Plotter(window_size=(1024, 768))
        elev_contours = self.contours.elevation()
        pl.add_mesh(elev_contours, scalars="Elevation", cmap="magma", smooth_shading=True)
        # Add skeleton as navy tubes
        for i1, i2 in self.edges:
            p1 = self.positions[i1]
            p2 = self.positions[i2]
            line = pv.Line(p1, p2)
            tube = line.tube(radius=0.2*self.node_radius)
            pl.add_mesh(tube, color="navy", opacity=0.4)
        # pl.set_background("darkgray")
        pl.set_background(Config.THEME.value)
        pl.show()

    def save_surface(self, filename):
        if self.contours:
            self.contours.save(filename)
            print(f"\tSurface saved to {filename}")

    def animate_bone_then_mesh_with_orbit(
        self,
        path="cave_bone_then_mesh_orbit.mp4",
        tube_color="navy",
        n_skip_bone=1,
        n_skip_mesh=1,
        mesh_opacity=0.4,
        orbit_frames=36,
        orbit_factor=2.0,
        color_map="fire"  # Optional: color map for mesh,
    ):
        """
        1. Animate only the skeleton ('bone') growing step by step.
        2. Hide the skeleton and animate only the mesh growing step by step.
        3. Optionally finish with a camera orbit of the final mesh.
        """
        if self.positions is None or self.edges is None:
            raise RuntimeError("\tYou must call load_graph() first.")

        margin = 2 * max(self.node_radius, self.edge_radius)
        mins = self.positions.min(axis=0) - margin
        maxs = self.positions.max(axis=0) + margin
        xs = np.arange(mins[0], maxs[0], self.voxel_size)
        ys = np.arange(mins[1], maxs[1], self.voxel_size)
        zs = np.arange(mins[2], maxs[2], self.voxel_size)
        grid_points = np.stack(
            np.meshgrid(xs, ys, zs, indexing="ij"), axis=-1
        ).reshape(-1, 3)
        vol_shape = (len(xs), len(ys), len(zs))

        pl = pv.Plotter(off_screen=True, window_size=(1920, 1080))
        pl.set_background("white")
        pl.enable_eye_dome_lighting()
        pl.show_axes()
        pl.open_movie(path, framerate=15, macro_block_size=1)

        # --- Step 1: Animate skeleton (bone) only ---
        print("\t\tAnimating skeleton (bone) growth...")
        skeleton_tubes = []
        for step, (i1, i2) in enumerate(tqdm(self.edges, desc="\t\t\tProgress")):
            if step % n_skip_bone != 0:
                continue
            a = self.positions[i1]
            b = self.positions[i2]
            line = pv.Line(a, b)
            tube = line.tube(radius=0.2 * self.node_radius)
            skeleton_tubes.append(tube)

            pl.clear()
            for tube in skeleton_tubes:
                pl.add_mesh(tube, color=tube_color, smooth_shading=True, lighting=True, style="wireframe", opacity=0.4)
            pl.camera_position = "iso"
            pl.write_frame()

        # --- Step 2: Animate mesh only (no bone visible) ---
        print("\n\t\tAnimating mesh growth(nodes)...")
        voxels = np.zeros(len(grid_points), dtype=bool)
        for idx, pos in enumerate(tqdm(self.positions, desc="\t\t\tProgress")):
            if idx % n_skip_mesh != 0:
                continue
            dists = np.linalg.norm(grid_points - pos, axis=1)
            voxels |= dists <= self.node_radius

            vol = voxels.reshape(vol_shape)
            vol_points = np.pad(vol, ((0,1), (0,1), (0,1)), mode="constant", constant_values=0)

            grid = pv.ImageData()
            grid.dimensions = vol_points.shape
            grid.origin = (xs[0], ys[0], zs[0])
            grid.spacing = (self.voxel_size, self.voxel_size, self.voxel_size)
            grid.point_data["cave"] = vol_points.flatten(order="F")

            contours = grid.contour(isosurfaces=[0.5], scalars="cave")
            if self.smoothing:
                contours = contours.smooth(n_iter=self.n_iter, relaxation_factor=self.relaxation_factor)

            pl.clear()
            if contours.n_points > 0:
                contours = contours.elevation()  # Color by elevation
                pl.add_mesh(contours, scalars="Elevation", cmap=color_map, smooth_shading=True, lighting=True, opacity=mesh_opacity)
            for tube in skeleton_tubes:
                pl.add_mesh(tube, color=tube_color, opacity=0.4)
            pl.camera_position = "iso"
            pl.write_frame()

        # Edges (tubes) need to be added to the mesh as well:
        def point_to_segment_dist(p, a, b):
            ap = p - a
            ab = b - a
            ab_dot = np.dot(ab, ab)
            if ab_dot == 0:
                return np.linalg.norm(ap)
            t = np.clip(np.dot(ap, ab) / ab_dot, 0, 1)
            closest = a + t * ab
            return np.linalg.norm(p - closest)

        print("\n\t\tAnimating mesh growth(edges)...")
        for step, (i1, i2) in enumerate(tqdm(self.edges, desc="\t\t\tProgress")):
            if step % n_skip_mesh != 0:
                continue
            a = self.positions[i1]
            b = self.positions[i2]
            rad = self.edge_radius
            seg_min = np.minimum(a, b) - rad
            seg_max = np.maximum(a, b) + rad
            mask = np.all((grid_points >= seg_min) & (grid_points <= seg_max), axis=1)
            points_in_box = grid_points[mask]
            if len(points_in_box) == 0:
                continue

            dists = np.array([point_to_segment_dist(p, a, b) for p in points_in_box])
            inside = dists <= rad
            voxels[mask] |= inside

            vol = voxels.reshape(vol_shape)
            vol_points = np.pad(vol, ((0,1), (0,1), (0,1)), mode="constant", constant_values=0)

            grid = pv.ImageData()
            grid.dimensions = vol_points.shape
            grid.origin = (xs[0], ys[0], zs[0])
            grid.spacing = (self.voxel_size, self.voxel_size, self.voxel_size)
            grid.point_data["cave"] = vol_points.flatten(order="F")

            contours = grid.contour(isosurfaces=[0.5], scalars="cave")
            if self.smoothing:
                contours = contours.smooth(n_iter=self.n_iter, relaxation_factor=self.relaxation_factor)

            pl.clear()
            if contours.n_points > 0:
                contours = contours.elevation()  # Color by elevation
                pl.add_mesh(contours, scalars="Elevation", cmap=color_map, smooth_shading=True, lighting=True, opacity=mesh_opacity)
            for tube in skeleton_tubes:
                pl.add_mesh(tube, color=tube_color, opacity=0.4)
            pl.camera_position = "iso"
            pl.write_frame()

        # --- Optional: Camera orbit of final mesh ---
        pl.clear()
        if contours.n_points > 0:
            contours = contours.elevation()  # Color by elevation
            pl.add_mesh(contours, scalars="Elevation", cmap=color_map, smooth_shading=True, lighting=True, opacity=mesh_opacity)


        center = contours.center
        radius = max(contours.length, 10) * orbit_factor
        n_frames = orbit_frames
        print("\n\t\tAnimating camera orbit around final mesh...")
        for i in tqdm(range(n_frames), desc="                Progress"):
            angle = 2 * math.pi * i / n_frames
            cam_x = center[0] + radius * math.cos(angle)
            cam_y = center[1] + radius * math.sin(angle)
            cam_z = center[2] + radius * 0.3  # keep it slightly above the center
            position = (cam_x, cam_y, cam_z)
            focal_point = center
            viewup = (0, 0, 1)
            pl.camera_position = (position, focal_point, viewup)
            pl.write_frame()


        pl.close()
        print(f"\t\t-Bone-then-mesh animation (with orbit) saved to {path}")


    def create_static_image(self, filename, tube_color="navy", mesh_opacity=1.0, color_map="fire"):
        """        
        Create a static image of the final mesh with skeleton tubes.
        """
        if self.positions is None or self.edges is None:
            raise RuntimeError("\tYou must call load_graph() first.")
        if self.contours is None:
            raise RuntimeError("\tYou must call extract_surface() first.")
        pl = pv.Plotter(off_screen=True, window_size=(1920, 1080))
        pl.set_background("white")
        pl.enable_eye_dome_lighting()
        pl.show_axes()
        elev_contours = self.contours.elevation()
        pl.add_mesh(elev_contours, scalars="Elevation", cmap=color_map, smooth_shading=True)
        # pl.add_mesh(self.contours, scalars="Elevation", cmap=color_map, smooth_shading=True, lighting=True, opacity=mesh_opacity)
        for i1, i2 in self.edges:
            p1 = self.positions[i1]
            p2 = self.positions[i2]
            line = pv.Line(p1, p2)
            tube = line.tube(radius=0.2 * self.node_radius)
            pl.add_mesh(tube, color=tube_color, opacity=0.4)
        pl.camera_position = "iso"
        pl.show(screenshot=filename)
        print(f"\tStatic image saved to {filename}") 
