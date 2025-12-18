# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 20:02:33 2025
[Description of the module or script]

@author: Mahdi Saadat
"""

import matplotlib.pyplot as plt


def plot_subsidence(X, Y, S):
    fig, ax = plt.subplots(figsize=(7, 6))

    levels = 20
    contour = ax.contourf(X, Y, S, levels=levels)
    plt.colorbar(contour, ax=ax, label="Subsidence (m)")

    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    ax.set_title("Predicted Vertical Subsidence")

    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.4)

    return fig
