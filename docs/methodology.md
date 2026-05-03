# Methodology

This document outlines the end-to-end data pipeline used to reconstruct and analyze the FUTO terrain.

## 1. Data Ingestion & Preprocessing
*   **Source Data:** 11 ground-truth VES survey points containing Longitude, Latitude, and Elevation (meters above sea level).
*   **Coordinate Transformation:** Raw WGS84 coordinates (degrees) were reprojected to **UTM Zone 32N** (meters). This Cartesian projection is strictly required to ensure distance calculations during interpolation are physically accurate.
*   **Grid Definition:** A 150×150 mesh grid was established over the bounding box of the survey area to serve as the target for interpolation.

## 2. Spatial Interpolation Engine
To convert the discrete points into a continuous surface, multiple interpolation algorithms were evaluated.
*   **Algorithm Selected:** Inverse Distance Weighting (IDW).
*   **Parameters:** A power parameter ($p = 2$) was utilized, dictating that the influence of a survey point diminishes with the square of its distance from the target grid cell.
*   **Validation:** Leave-One-Out Cross-Validation (LOOCV) was employed to systematically hide one data point, predict its value using the remaining 10, and calculate the Root Mean Square Error (RMSE).

## 3. Environmental Simulation (Hazard Modeling)
The interpolated elevation grid served as the baseline for three distinct vulnerability models, generated via weighted overlays:

*   **Flood Susceptibility:**
    *   Elevation (45%) + Slope (35%) + Terrain Class (20%)
*   **Erosion Susceptibility:**
    *   Slope (55%) + Elevation (25%) + Terrain Class (20%)
*   **Urban Expansion Pressure:**
    *   Calculated using a proxy of topographical safety (low flood/erosion risk) and terrain accessibility.

## 4. Generative Integration
The final 2D arrays were parsed to generate `.obj` mesh files and corresponding texture maps. The derived zonal statistics were systematically formatted into descriptive text prompts to guide generative AI models in creating accurate visual representations of the simulated FUTO environment.
