# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 20:00:18 2025
[Description of the module or script]

@author: Mahdi Saadat
"""

import numpy as np
from scipy.special import erf
import pandas as pd




def get_subsidence_factor(calculated_ratio, hard_rock_percentage):
    """
    Calculates W/h and retrieves the corresponding value from the table.
    
    Parameters:
    W (float): Width value
    h (float): Height value
    top_row_val (float): The column header to look up (0.1, 0.2, etc.)
    """
    
    # 1. Define the table data
    data = {
        'W/h': [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        0.1: [0.64, 0.69, 0.71, 0.72, 0.73, 0.74, 0.74, 0.74, 0.75, 0.75, 0.75, 0.75, 0.75, 0.76, 0.76],
        0.2: [0.59, 0.63, 0.65, 0.66, 0.67, 0.68, 0.68, 0.68, 0.69, 0.69, 0.69, 0.69, 0.69, 0.69, 0.69],
        0.3: [0.51, 0.55, 0.57, 0.58, 0.58, 0.59, 0.59, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60, 0.60],
        0.4: [0.42, 0.46, 0.47, 0.48, 0.49, 0.49, 0.49, 0.49, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50],
        0.5: [0.34, 0.36, 0.38, 0.38, 0.39, 0.39, 0.39, 0.40, 0.40, 0.40, 0.40, 0.40, 0.40, 0.40, 0.40],
        0.6: [0.26, 0.28, 0.29, 0.30, 0.30, 0.31, 0.31, 0.31, 0.31, 0.31, 0.31, 0.31, 0.31, 0.31, 0.31],
        0.7: [0.21, 0.22, 0.23, 0.23, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24, 0.24],
        0.8: [0.16, 0.18, 0.18, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19]
    }
    df = pd.DataFrame(data).set_index('W/h')

    # 2. Find the closest W/h index in the table
    # This prevents errors if W/h is something like 0.92
    available_ratios = df.index.tolist()
    closest_ratio = min(available_ratios, key=lambda x: abs(x - calculated_ratio))

    # 3. Find the closest column header
    available_cols = [float(c) for c in df.columns]
    closest_col = min(available_cols, key=lambda x: abs(x - hard_rock_percentage))

    # 4. Return the value
    return df.at[closest_ratio, closest_col]


# #--------------------- Depth of Cover ----------------

# """
#     This depth of cover can be modified later
# """
# # Your initial data
# data = [
#     {
#         "Panel ID": 1,
#         "Panel ID LW": "LW03",
#         "Start": 230,
#         "End": 130,
#         "Seam": "Seam A"
#     }
# ]

# df_doc = pd.DataFrame(data)
# #--------------------- End of Depth of Cover ----------------


# # Define your grid points
# grid_point = 10 

# # Initialize your storage dictionary
# gradient_dict = {}

# def calculate_gradient(start, end, num_points=grid_point):
#     return np.linspace(start, end, num_points)


# # Populate the dictionary with gradients
# for index, row in df_doc.iterrows():
#     lw_id = row['Panel ID']
#     gradient = calculate_gradient(row['Start'], row['End'])
#     gradient_dict[lw_id] = gradient

# # Dictionary to store inflection points with Panel ID as the key
# inflection_points_dict = {}
# for ip, (lw_id, igrad) in zip(range(len(all_panel_widths)), gradient_dict.items()):
#     inflection_points_list = []
#     current_panel_id = ip + 1
#     current_row = df_doc[df_doc['Panel ID'] == current_panel_id]
    
#     if not current_row.empty:
#         mystart = current_row['Start'].values[0]
#         myend = current_row['End'].values[0]   
#     else:
#         #print(f"Panel ID {current_panel_id} not found in the dataframe.")
#         continue  # Skip this panel if it isn't found
    
#     avg_doc = (mystart + myend) / 2
    
#     i_width = all_panel_widths[ip]
#     w_h_ratio = round(i_width / avg_doc, 1)
#     #print(f"Panel width: {i_width} , Average DOC: {avg_doc}, W/H Ratio: {w_h_ratio}, Panel_id: {lw_id}, Panel_id: {ip}")
#     if w_h_ratio >= 1.2:
        
#         inf_point = igrad * 0.2
#     else:
#         inf_point = np.round(
#             igrad * (-2.1702 * (w_h_ratio**4) + 7.2849 * (w_h_ratio**3) - 9.1824 * (w_h_ratio**2) + 5.3794 * w_h_ratio - 1.1308), 
#             3
#         )
#     # Append inf_point to the list
#     inflection_points_list.append(inf_point)
#     # Store the list in the dictionary
#     inflection_points_dict[lw_id] = inflection_points_list
    
#     print(f"W/h : {w_h_ratio}, Inflection Point: {inflection_points_list}")

# beta_angle_dict = {}
# major_influence_radius_dict = {}
# m_to_ft = 3.28084  # meters to feet
# ft_to_m = 0.3048   # feet to meters

# doc_counter = 0
# # Calculate beta_angle and major influence radius for each depth of cover
# for panel_id, gradient in gradient_dict.items():
#     major_influence_radius_list = []  # Initialize a new list for each panel ID
#     # Calculate beta_angle (angle of major influence) in degrees
#     gradient_ft = gradient * m_to_ft

#     beta_angle = 58.89 + 0.03089 * gradient_ft - 0.0000184 * (gradient_ft ** 2)

#     # Convert beta_angle from degrees to radians
#     beta_angle_radians = np.radians(beta_angle)
    
#     # Store beta_angle value in the dictionary
#     beta_angle_dict[doc_counter] = beta_angle
    
#     # Calculate major influence radius
#     major_influence_radius = np.round(gradient / np.tan(beta_angle_radians), 2)
#     major_influence_radius_list.append(major_influence_radius)
#     # Store major influence radius in the dictionary
#     major_influence_radius_dict[panel_id] = major_influence_radius_list
#     doc_counter +=1


# def calculate_subsidence(lw_panel_id, panel_width, panel_length, extraction_thick, percentage_hard_rock, depth_of_cover,grid_resolution=100):
#     global my_panel_id
#     my_panel_id = lw_panel_id
#     myrow = df_doc[df_doc['Panel ID'] == my_panel_id]
    
#     #If the row exists, extract Start and End values
#     if not myrow.empty:
#         mystart = myrow['Start'].values[0]
#         myend = myrow['End'].values[0]   
#     else:
#         print(f"Panel ID {my_panel_id} not found in the dataframe.")
    
#     average_depth_of_cover = (mystart+myend)/2
    
#     # Define buffers
#     x_buffer = 100#0.85 * panel_length
#     y_buffer = 100#1.5 * panel_width
    
#     # Define x and y ranges
#     global x_values_limit
#     global y_values_limit
#     x_values_limit = np.linspace(0 - x_buffer, panel_length + x_buffer, grid_resolution)
#     y_values_limit = np.linspace(0 - y_buffer, panel_width + y_buffer, grid_resolution)
    

#     w_h_rat = round(panel_width / average_depth_of_cover, 1)
#     hr_percentage = percentage_hard_rock/100
#     subsidence_factor = get_subsidence_factor(w_h_rat,hr_percentage)
    
#     # Calculate Smax, Maximum Subsidence [m]
#     s_max = round(extraction_thick * subsidence_factor, 1)
#     X, Y = np.meshgrid(x_values_limit, y_values_limit)
#     Sxy = np.zeros_like(X)
    
#     inflection_point_list = inflection_points_dict[lw_panel_id]
#     major_influence_radius_array = major_influence_radius_dict[lw_panel_id]
    
#     # Iterate over x and y values
#     for i, x in enumerate(x_values_limit):
#         inflection_point_to_edge_conservative = inflection_point_list[0][i]
#         major_influence_radius = major_influence_radius_array[0][i]
#         for j, y in enumerate(y_values_limit):
            
#             x = x_values_limit[i]
#             y = y_values_limit[j]
            
#             Sxy[i, j] = -s_max * (
#                 0.5 * (erf(np.sqrt(np.pi) * (inflection_point_to_edge_conservative - y) / major_influence_radius) +
#                        erf(np.sqrt(np.pi) * (-panel_width + inflection_point_to_edge_conservative + y) / major_influence_radius))
#             ) * (
#                 0.5 * (erf(np.sqrt(np.pi) * (inflection_point_to_edge_conservative - x) / major_influence_radius) +
#                        erf(np.sqrt(np.pi) * (-panel_length + inflection_point_to_edge_conservative + x) / major_influence_radius))
#             )
            
#     return X, Y, Sxy




def calculate_subsidence(
    panel_width,
    panel_length,
    depth_of_cover,
    extraction_thickness,
    percentage_hard_rock,
    uploaded_panel_dxf,
    uploaded_parts_dxf,
    grid_points=200
):
    """
    Pure subsidence calculation function (NO plotting).

    Returns:
        X, Y : meshgrid coordinates
        S    : subsidence values (negative)
    """

    # --- Basic checks ---
    if panel_width <= 0 or panel_length <= 0:
        raise ValueError("Panel dimensions must be positive.")
    if depth_of_cover <= 0:
        raise ValueError("Depth of cover must be positive.")
    if extraction_thickness <= 0:
        raise ValueError("Extraction thickness must be positive.")

    # --- W/H ratio ---
    w_h = panel_width / depth_of_cover
    
    # --- Inflection distance logic (conservative, matches your code) ---
    if w_h >= 1.2:
        inflection = 0.2 * depth_of_cover
    else:
        inflection = depth_of_cover * (
            -2.1702 * w_h**4
            + 7.2849 * w_h**3
            - 9.1824 * w_h**2
            + 5.0921 * w_h
            - 0.0134
        )
    # Calculate the subsidence factor
    w_h_rat = round(panel_width / depth_of_cover, 1)
    hr_percentage = percentage_hard_rock/100
    subsidence_factor = get_subsidence_factor(w_h_rat,hr_percentage)
    
    # --- Maximum subsidence ---
    S_max = -subsidence_factor * extraction_thickness

    # --- Grid ---
    x = np.linspace(-panel_width, panel_width, grid_points)
    y = np.linspace(-panel_length, panel_length, grid_points)
    X, Y = np.meshgrid(x, y)

    # --- Influence functions ---
    Fx = 0.5 * (1 + erf((panel_width / 2 - np.abs(X)) / inflection))
    Fy = 0.5 * (1 + erf((panel_length / 2 - np.abs(Y)) / inflection))

    S = S_max * Fx * Fy

    return X, Y, S
