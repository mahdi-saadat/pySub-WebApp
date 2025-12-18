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
