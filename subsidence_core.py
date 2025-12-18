# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 20:00:18 2025
[Description of the module or script]

@author: Mahdi Saadat
"""

import numpy as np
from scipy.special import erf


def calculate_subsidence(
    panel_width,
    panel_length,
    depth_of_cover,
    extraction_thickness,
    subsidence_factor,
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
