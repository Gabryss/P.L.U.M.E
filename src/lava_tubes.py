# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
from scipy.ndimage import gaussian_filter
import pyvista as pv
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import json

class ProceduralLavaTube:
    def __init__(
        self, 
        shape=(120, 60, 40), 
        tube_major_radius=2.4, 
        tube_minor_radius=1.4, 
        min_neck_minor=1.0, 
        chamber_major=3.5, 
        chamber_minor=2.1,
        seed=None
    ):
        self.shape = shape
        self.tube_major_radius = tube_major_radius      # X (and Y, since Y is along tube)
        self.tube_minor_radius = tube_minor_radius      # Z (vertical)
        self.min_neck_minor = min_neck_minor            # Min allowed for minor axis at necks
        self.chamber_major = chamber_major
        self.chamber_minor = chamber_minor
        if seed is not None:
            np.random.seed(seed)
        self.reset()

    def reset(self):
        self.volume = np.ones(self.shape, dtype=np.uint8)
        self.paths = []

    def generate_main_path(self, length=100, amplitude=12, freq=0.08, center_y=None, center_z=None):
        if center_y is None:
            center_y = self.shape[1] // 2
        if center_z is None:
            center_z = self.shape[2] // 2
        x = np.arange(length)
        y = center_y + amplitude * np.sin(freq * x) + np.random.randn(length) * 0.7
        z = center_z + 3.5 * np.sin(freq * x + 1.2) + np.random.randn(length) * 0.5
        main_path = np.stack([x, y, z], axis=1)
        self.main_path = main_path
        self.paths.append(('main', main_path, self.tube_major_radius, self.tube_minor_radius))
        return main_path

    def add_side_branches(self, n_branches=2, min_length=18, max_length=36, min_offset=6, max_offset=14, p_rejoin=0.7):
        main_len = len(self.main_path)
        for i in range(n_branches):
            # Randomly pick branch start and length
            leave = np.random.randint(10, main_len - max_length - 10)
            blen = np.random.randint(min_length, max_length+1)
            rejoin = leave + blen
            if rejoin > main_len - 3:
                rejoin = main_len - 3
            # Branch is offset from main, can arc and then possibly rejoin
            branch_path = self.main_path[leave:rejoin].copy()
            offset = np.random.uniform(min_offset, max_offset)
            arc = np.sin(np.linspace(0, np.pi, blen))  # arc shape in Y
            branch_path[:, 1] += offset * arc
            # Small Z arc for vertical offset variety
            branch_path[:, 2] += np.random.uniform(-2.0, 2.5) * arc
            # Optionally, rejoin by reducing offset toward end of branch
            if p_rejoin > 0 and np.random.rand() < p_rejoin:
                arc2 = np.sin(np.linspace(np.pi, 2*np.pi, blen))
                branch_path[:, 1] += -offset * 0.85 * arc2  # back toward main
                branch_path[:, 2] += np.random.uniform(-2.0, 2.5) * arc2
            # Elliptical: Use same or slightly varied axes as main tube
            major = self.tube_major_radius * np.random.uniform(0.9, 1.1)
            minor = self.tube_minor_radius * np.random.uniform(0.9, 1.1)
            self.paths.append((f'branch{i+1}', branch_path, major, minor))

    def carve_tubes(
        self, 
        n_chambers=3, chamber_major=None, chamber_minor=None, 
        n_necks=2, neck_minor=None
    ):
        # Defaults if not set
        if chamber_major is None: chamber_major = self.chamber_major
        if chamber_minor is None: chamber_minor = self.chamber_minor
        if neck_minor is None: neck_minor = self.min_neck_minor

        for name, path, base_major, base_minor in self.paths:
            plen = len(path)
            # Pick random chambers and necks
            chamber_population = np.arange(10, plen-10)
            chamber_count = min(n_chambers, len(chamber_population))
            chamber_idx = np.random.choice(chamber_population, size=chamber_count, replace=False) if chamber_count > 0 else []

            neck_population = np.arange(8, plen-8)
            neck_count = min(n_necks, len(neck_population))
            neck_idx = np.random.choice(neck_population, size=neck_count, replace=False) if neck_count > 0 else []

            
            for i, pt in enumerate(path):
                # Vary axes for natural look
                a = base_major + 0.6 * np.sin(0.2*i + np.random.uniform(-0.6, 0.6))
                b = base_minor + 0.4 * np.sin(0.2*i + np.random.uniform(-0.6, 0.6))
                a += np.random.uniform(-0.2, 0.2)
                b += np.random.uniform(-0.2, 0.2)
                # Chambers
                if i in chamber_idx:
                    a += chamber_major * np.random.uniform(0.7, 1.0)
                    b += chamber_minor * np.random.uniform(0.7, 1.0)
                # Necks
                if i in neck_idx:
                    b = max(b - (base_minor - neck_minor) * np.random.uniform(0.9, 1.3), neck_minor)
                # No negative or zero axes!
                a = max(a, 0.6)
                b = max(b, self.min_neck_minor)
                cx, cy, cz = pt
                # Elliptical carve in X-Z, circle in Y
                for x in range(int(np.floor(cx-a)), int(np.ceil(cx+a))+1):
                    for y in range(int(np.floor(cy-base_major)), int(np.ceil(cy+base_major))+1):
                        for z in range(int(np.floor(cz-b)), int(np.ceil(cz+b))+1):
                            if (0 <= x < self.shape[0]) and (0 <= y < self.shape[1]) and (0 <= z < self.shape[2]):
                                ellipse = ((x-cx)/a)**2 + ((z-cz)/b)**2 + ((y-cy)/base_major)**2
                                if ellipse <= 1.0:
                                    self.volume[x, y, z] = 0

    def smooth(self, sigma=1.15):
        smooth = gaussian_filter(self.volume.astype(float), sigma=sigma)
        self.mask = (smooth < 0.5).astype(np.uint8)

    def plot_3d(self):
        grid = pv.ImageData()
        grid.dimensions = np.array(self.mask.shape) + 1
        grid.origin = (0, 0, 0)
        grid.spacing = (1, 1, 1)
        grid.cell_data["values"] = self.mask.flatten(order="F")
        grid = grid.cell_data_to_point_data()
        tube_mesh = grid.contour(isosurfaces=[0.5])
        tube_mesh.plot(opacity=1.0)

    def scroll_cross_section(self):
        fig, ax = plt.subplots(figsize=(6,5))
        plt.subplots_adjust(bottom=0.18)
        init_x = self.shape[0] // 2
        slice_img = 1 - self.mask[init_x, :, :].T
        im = ax.imshow(slice_img, cmap='gray', origin='lower', aspect='auto')
        ax.set_title(f"2D Cross-section at x={init_x} (compare to Huehue Cave)")
        ax.set_xlabel("Y")
        ax.set_ylabel("Z")
        ax_slider = plt.axes([0.22, 0.05, 0.6, 0.04], facecolor="lightgoldenrodyellow")
        slice_slider = Slider(ax_slider, 'X Slice', 0, self.shape[0]-1, valinit=init_x, valstep=1)
        def update(val):
            idx = int(slice_slider.val)
            slice_img = 1 - self.mask[idx, :, :].T
            im.set_data(slice_img)
            ax.set_title(f"2D Cross-section at x={idx} (compare to Huehue Cave)")
            fig.canvas.draw_idle()
        slice_slider.on_changed(update)
        plt.show()



    def export_skeleton_json(self, filename=None, generation_name="LavaTube_Generation", selected_algorithm="procedural_spline"):
        # Collect all points from paths and assign unique node IDs
        node_list = []
        node_map = {}  # (path_idx, point_idx): node_id
        edges = []
        next_node_id = 0

        # Track parent for each node (main path = parent None, branches = where they leave main)
        for path_idx, (name, path, major, minor) in enumerate(self.paths):
            parent_ids = [None]  # For main path, first parent is None
            if path_idx > 0:
                # For branches, parent is the main node at branch start
                parent_ids = [None]  # can be improved for precise graph connectivity

            for i, pt in enumerate(path):
                node_id = next_node_id
                node_map[(path_idx, i)] = node_id

                # For edges (connection to previous node in path)
                if i > 0:
                    edges.append((node_id-1, node_id))

                node_list.append({
                    "id": node_id,
                    "parent": node_id-1 if i > 0 else None,  # parent in the same path
                    "edges": [node_id-1] if i > 0 else [],
                    "coordinates": {"x": float(pt[0]), "y": float(pt[1]), "z": float(pt[2])},
                    "radius": float((major + minor) / 2),  # You can export both axes if you want
                    "active": True
                })
                next_node_id += 1

        # Now set edges for each node correctly (and fix parents/edges for branches if needed)
        nodes = {str(node["id"]): node for node in node_list}

        # Final JSON structure, similar to your sample
        output_json = {
            "generation_name": generation_name,
            "date": "YYYY_MM_DD_HH_MM_SS",  # can fill with datetime.now().strftime
            "generation_size": list(self.shape),
            "generation_dimension": "3D",
            "generation_type": "LAVATUBE",
            "selected_algorithm": selected_algorithm,
            "nodes_number": len(node_list),
            "nodes_radius": (self.tube_major_radius + self.tube_minor_radius) / 2,
            "nodes": nodes
        }

        if filename:
            with open(filename, "w") as f:
                json.dump(output_json, f, indent=2)
        return output_json



# --- Example usage ---
if __name__ == "__main__":
    
    tube = ProceduralLavaTube(
        shape=(240, 100, 64), 
        tube_major_radius=4.8, 
        tube_minor_radius=2.6, 
        min_neck_minor=1.7, 
        chamber_major=6.3,
        chamber_minor=4.1,
        seed=42
    )
    tube.generate_main_path(length=210)
    tube.add_side_branches(
        n_branches=8,            # Many branches!
        min_length=18, max_length=45,
        min_offset=8, max_offset=21,
        p_rejoin=0.85
    )
    tube.carve_tubes(n_chambers=10, chamber_major=6.2, chamber_minor=4.0, n_necks=9, neck_minor=2.0)
    tube.smooth(sigma=1.45)
    tube.plot_3d()
    tube.scroll_cross_section()
    skeleton = tube.export_skeleton_json(filename="skeleton.json")
    print(skeleton)

