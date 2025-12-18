# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 20:02:33 2025
[Description of the module or script]

@author: Mahdi Saadat
"""
import matplotlib
matplotlib.use("Agg")  # REQUIRED for Streamlit Cloud

import matplotlib.pyplot as plt
from collections import defaultdict
import os
import ezdxf
import numpy as np

# Global variables to store aggregated results
all_panel_widths = []
all_panel_lengths = []
all_pillar_spacings = []

def calculate_dimensions(vertices):
    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]
    if x_coords and y_coords:
        length = max(x_coords) - min(x_coords)
        width = max(y_coords) - min(y_coords)
        #print(f"✔Pane width: {width}")
        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)
        return length, width, min_x, max_x, min_y, max_y
    else:
        return None, None, None, None, None, None

def find_panel_lines(lines):
    panels_temp = []
    line_dict = defaultdict(list)
    for line in lines:
        p1, p2 = line.dxf.start, line.dxf.end
        line_dict[(p1.x, p1.y)].append((p2.x, p2.y))
        line_dict[(p2.x, p2.y)].append((p1.x, p1.y))
    
    visited = set()
    for start, ends in line_dict.items():
        if start in visited:
            continue
        panel = [start]
        visited.add(start)
        current = start
        while len(panel) < 4:
            for end in line_dict[current]:
                if end not in visited:
                    panel.append(end)
                    visited.add(end)
                    current = end
                    break
        
        # Ensure the panel is a rectangle by checking the number of vertices
        if len(panel) == 4:
            panels_temp.append(panel)
    
    # Calculate dimensions and sort panels based on min_y
    global sorted_panels
    panels = [(panel, calculate_dimensions(panel)) for panel in panels_temp]
    panels_sorted = sorted(panels, key=lambda x: x[1][4])  # Sorting by min_y
    sorted_panels = [panel[0] for panel in panels_sorted]
    return sorted_panels

def calculate_pillar_spacing(panels):
    min_y_values = []
    max_y_values = []
    for panel in panels:
        _, _, _, _, min_y, max_y = calculate_dimensions(panel)
        min_y_values.append(min_y)
        max_y_values.append(max_y)
    
    pillar_spacings = [abs(min_y_values[i + 1] - max_y_values[i]) for i in range(len(min_y_values) - 1)]
    
    # Add the width of the last panel as the spacing next to it
    if panels:
        last_panel_width = max_y_values[-1] - min_y_values[-1]
        pillar_spacings.append(last_panel_width)
    
    return pillar_spacings



def process_dxf_files(directory):
    global all_panel_widths, all_panel_lengths, all_panel_min_x, all_panel_max_x, all_panel_min_y, all_panel_max_y, all_pillar_spacings

    # Reset the global variables to store new results
    all_panel_widths = []
    all_panel_lengths = []
    all_panel_min_x = []
    all_panel_max_x = []
    all_panel_min_y = []
    all_panel_max_y = []
    all_pillar_spacings = []

    # Loop through all DXF files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".dxf"):
            dxf_path = os.path.join(directory, filename)
            #dxf_letter = filename.split('_')[0][-1] 
            #print(dxf_letter)
            try:
                doc = ezdxf.readfile(dxf_path)
            except IOError:
                print(f"Error: Cannot open {dxf_path}. Check if the file exists.")
                continue

            msp = doc.modelspace()
            lines = list(msp.query("LINE"))

            # Process panels in this DXF file
            panels = find_panel_lines(lines)
            panel_widths = []
            panel_lengths = []
            panel_min_x = []
            panel_max_x = []
            panel_min_y = []
            panel_max_y = []
            for panel in panels:
                length, width, min_x, max_x, min_y, max_y = calculate_dimensions(panel)
                panel_widths.append(width)
                panel_lengths.append(length)
                panel_min_x.append(min_x)
                panel_max_x.append(max_x)
                panel_min_y.append(min_y)
                panel_max_y.append(max_y)
                #print(f"File: {filename}, Panel Width: {width}, Panel Length: {length}, Min X: {min_x}, Max X: {max_x}, Min Y: {min_y}, Max Y: {max_y}")

            # Plot panels for the current DXF file
            #plot_panels(panels,dxf_letter)

            # Calculate and aggregate pillar spacings
            panel_pillar_spacings = calculate_pillar_spacing(panels)
            all_pillar_spacings.extend(panel_pillar_spacings)

            # Aggregate panel widths and lengths
            all_panel_widths.extend(panel_widths)
            all_panel_lengths.extend(panel_lengths)
            all_panel_min_x.extend(panel_min_x)
            all_panel_max_x.extend(panel_max_x)
            all_panel_min_y.extend(panel_min_y)
            all_panel_max_y.extend(panel_max_y)


#process_dxf_files(dxf_directory_for_calculations)

#---------------------------------------------------------------------- End DXF Analysis ---------------------------------------------------------------------

ploting_panels = []
def process_dxf_files(directory):

    # Loop through all DXF files in the specified directory
    for filename in os.listdir(directory):
            # Process panels in this DXF file
            if filename.endswith(".dxf"):
                dxf_path = os.path.join(directory, filename)
                #dxf_letter = filename.split('_')[0][-1] 
                #print(dxf_letter)
                try:
                    doc = ezdxf.readfile(dxf_path)
                except IOError:
                    print(f"Error: Cannot open {dxf_path}. Check if the file exists.")
                    continue

                msp = doc.modelspace()
                lines = list(msp.query("LINE"))
            temp_panel = find_panel_lines(lines)
            ploting_panels.append(temp_panel)

# Rotation function for panels
def rotate_panel(panel, angle_deg, ref_point=(0, 0)):
    """Rotate the panel's coordinates by a specified angle around a reference point."""
    theta = np.radians(angle_deg)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta), np.cos(theta)]])
    
    # Translate panel coordinates to rotate around reference point
    panel_rotated = []
    for x, y in panel:
        x_shifted, y_shifted = x - ref_point[0], y - ref_point[1]  # Translate to reference point
        x_rotated, y_rotated = rotation_matrix @ np.array([x_shifted, y_shifted])
        panel_rotated.append((x_rotated + ref_point[0], y_rotated + ref_point[1]))  # Translate back
    
    return panel_rotated

# Function to plot panel outlines with rotation
def plot_panels_dxf(ax, panels, angle_deg):
    for panel in panels:
        # Rotate the panel by the specified angle
        rotated_panel = rotate_panel(panel, angle_deg)

        # Plot the rotated panel
        x_coords, y_coords = zip(*rotated_panel)
        x_coords += (x_coords[0],)  # Close the polygon
        y_coords += (y_coords[0],)
        ax.plot(x_coords, y_coords, color='black', linewidth=1.5)

#----------------------------------------------------------------------
#process_dxf_files(dxf_directory_for_calculations)
#------------------------------------------------------- DXF Processing for LW Geometries

def rotate_point_for_LW(point, angle, center):
    # (This function remains the same)
    angle_rad = np.radians(angle)
    x, y = point
    cx, cy = center
    x_translated = x - cx
    y_translated = y - cy
    x_rotated = x_translated * np.cos(angle_rad) - y_translated * np.sin(angle_rad)
    y_rotated = x_translated * np.sin(angle_rad) + y_translated * np.cos(angle_rad)
    x_final = x_rotated + cx
    y_final = y_rotated + cy
    return (x_final, y_final)

def plot_rotated_dxf_LW_lines_check(directory, angle, ax=None, line_color='k'):
    # Added line_color argument, default is 'k' (black)
    if ax is None:
        fig, ax = plt.subplots()

    all_x_coords = []
    all_y_coords = []
    
    # Pass 1: Collect all coordinates to determine the Min/Max bounds
    for filename in os.listdir(directory):
        if filename.endswith(".dxf"):
            dxf_path = os.path.join(directory, filename)
            try:
                doc = ezdxf.readfile(dxf_path)
            except (IOError, ezdxf.DXFStructureError) as e:
                print(f"Skipping {dxf_path} due to error: {e}")
                continue

            msp = doc.modelspace()
            lines = msp.query("LINE")

            for line in lines:
                all_x_coords.extend([line.dxf.start.x, line.dxf.end.x])
                all_y_coords.extend([line.dxf.start.y, line.dxf.end.y])

    # Calculate the rotation center (bottom-left corner)
    if all_x_coords and all_y_coords:
        center_x = min(all_x_coords)
        center_y = min(all_y_coords)
        rotation_center = (center_x, center_y)
        #print(f"Rotation Center for DXF in {directory}: {rotation_center}")

        # Pass 2: Plot the rotated lines
        for filename in os.listdir(directory):
            if filename.endswith(".dxf"):
                dxf_path = os.path.join(directory, filename)
                try:
                    doc = ezdxf.readfile(dxf_path)
                except (IOError, ezdxf.DXFStructureError) as e:
                    continue

                msp = doc.modelspace()
                lines = msp.query("LINE")

                for line in lines:
                    start_rotated = rotate_point_for_LW((line.dxf.start.x, line.dxf.start.y), angle, rotation_center)
                    end_rotated = rotate_point_for_LW((line.dxf.end.x, line.dxf.end.y), angle, rotation_center)
                    
                    # *** FIX: Use line_color variable here ***
                    ax.plot([start_rotated[0], end_rotated[0]], 
                            [start_rotated[1], end_rotated[1]], 
                            color=line_color, linestyle='-', linewidth=1.5) # Increased linewidth slightly for visibility

        ax.set_aspect('equal')
    else:
        print(f"No DXF lines found in directory: {directory}")


#-----------------------------------------------------------------------------------------------------------------------------------------
def plot_subsidence(X, Y, S):
    fig, ax = plt.subplots(figsize=(10, 5))

    levels = 20
    contour = ax.contourf(X, Y, S, levels=levels)
    plt.colorbar(contour, ax=ax, label="Subsidence (m)")

    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    ax.set_title("Predicted Vertical Subsidence")

    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.4)

    return fig
#-----------------------------------------------------------------------------------------------------------------------------------------
