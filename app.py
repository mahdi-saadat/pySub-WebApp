# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 20:03:04 2025
[Description of the module or script]

@author: Mahdi Saadat
"""

import streamlit as st

# -------------------------------------------------
# Page config (ONLY ONCE, FIRST THING)
# -------------------------------------------------
st.set_page_config(
    page_title="pySub – Subsidence Assessment",
    layout="centered"
)

# -------------------------------------------------
# Basic UI (render immediately)
# -------------------------------------------------
st.title("pySub – Subsidence Assessment Tool")
st.write("App started successfully")

# -------------------------------------------------
# Import heavy modules AFTER UI is visible
# -------------------------------------------------
from subsidence_core import calculate_subsidence
from plotting import plot_subsidence

st.success("Modules imported successfully")

st.markdown("### Enter panel and geotechnical parameters")

# -------------------------------------------------
# Inputs
# -------------------------------------------------
panel_width = st.number_input("Panel width (m)", 50.0, 1000.0, 270.0)
panel_length = st.number_input("Panel length (m)", 50.0, 5000.0, 1000.0)
depth_of_cover = st.number_input("Depth of cover (m)", 50.0, 1000.0, 115.0)
extraction_thickness = st.number_input("Extraction thickness (m)", 1.0, 10.0, 4.20)
percentage_hard_rock = st.number_input("Hard Rock Percentage", 10.0, 100.0, 30.0)
# -------------------------------------------------
# Run model
# -------------------------------------------------
if st.button("Run Subsidence Assessment"):
    with st.spinner("Running subsidence model..."):
        try:
            X, Y, S = calculate_subsidence(
                panel_width,
                panel_length,
                depth_of_cover,
                extraction_thickness,
                percentage_hard_rock
            )

            fig = plot_subsidence(X, Y, S)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")
