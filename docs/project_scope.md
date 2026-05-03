# Project Scope: GeoSim FUTO

## 1. Executive Summary
GeoSim FUTO is a geospatial data science initiative designed to reconstruct the topography of the Federal University of Technology Owerri (FUTO) and its immediate surroundings. Utilizing a sparse dataset of 11 Vertical Electrical Sounding (VES) elevation points, the project builds a continuous 3D terrain surface to model environmental vulnerabilities, including flood susceptibility, erosion risk, and urban expansion pressure.

## 2. Objectives
*   **Terrain Reconstruction:** Transform discrete field survey data into a continuous 150×150 elevation grid using spatial interpolation.
*   **Hazard Simulation:** Develop weighted overlay models to categorize the campus into varying risk zones for flooding and soil erosion.
*   **Predictive Zoning:** Analyze urban expansion pressure based on topographic safety and accessibility.
*   **Asset Generation:** Export the analyzed spatial data into 3D-ready formats (.obj) and AI-generative prompts for immersive visualization.

## 3. Toolstack & Environment
To ensure reproducibility and bypass local hardware constraints, the pipeline is engineered for cloud-native and open-source execution:
*   **Processing Environment:** Google Colab (Python)
*   **Spatial Analysis:** QGIS (Desktop validation and mapping)
*   **Core Libraries:** `numpy`, `pandas`, `scipy` (spatial/interpolate), `pyproj` (coordinate transformation)

## 4. Deliverables
1.  Validated spatial interpolation pipeline (Python).
2.  Interactive topographical visualizations.
3.  Categorized risk maps (Flood, Erosion, Urban Pressure).
4.  3D mesh exports and generative AI scene prompts grounded in the derived spatial data.
