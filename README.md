# GeoSim FUTO

A Generative AI-Enhanced GIS Project for 3D Terrain Reconstruction and Environmental Change Simulation around the Federal University of Technology Owerri (FUTO), Nigeria.

## Overview

GeoSim FUTO is a geospatial data science project that transforms real elevation point data from the FUTO environment into an interactive 3D terrain model. The project combines GIS, Python, environmental simulation, and Generative AI concepts to build an immersive system capable of visualizing terrain and simulating environmental change.

This project was developed as a learning-driven exploration of how geospatial data can be reconstructed into meaningful 3D environments and enhanced for future AR/VR applications.

## Project Aim

To develop a GIS-based system that reconstructs the FUTO terrain from elevation point data, simulates environmental change, and explores the use of Generative AI for immersive geospatial visualization.

## Objectives

- Clean and organize real-world geospatial elevation data from the FUTO area
- Interpolate scattered elevation points into a continuous terrain surface
- Visualize the terrain in 2D and 3D
- Simulate environmental change scenarios such as flood vulnerability
- Explore the integration of Generative AI for scene enrichment and future immersive visualization
- Build a reproducible project structure suitable for research and portfolio presentation

## Study Area

The study area covers locations around the Federal University of Technology Owerri (FUTO) and surrounding communities in Imo State, Nigeria, including Eziobodo, Obinze, Avu, Nekede, and Ihiagwa.

## Dataset

The dataset currently consists of sampled elevation points with the following attributes:

- Longitude
- Latitude
- Elevation (m)
- Location name

Example data points include:
- Church, Eziobodo
- Girls Secondary School, Eziobodo
- Gas Plant, Avu
- Behind Geology Building, FUTO

## Methodology

The project workflow follows these stages:

1. Data collection and cleaning  
   Elevation point data is structured into a clean tabular dataset.

2. Terrain interpolation  
   Spatial interpolation methods are applied to estimate unknown elevation values between known sample points.

3. Terrain visualization  
   The interpolated surface is visualized as a 2D surface map and a 3D terrain model.

4. Environmental simulation  
   Terrain-based simulations are performed to identify environmentally vulnerable zones, such as low-lying flood-prone areas.

5. Generative AI integration  
   Generative AI concepts are introduced to enrich the terrain scene, generate plausible environmental scenarios, and support immersive AR/VR-style experiences.

## Tools and Technologies

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy
- GIS concepts and terrain modeling
- HTML-based interactive visualization
- Generative AI concepts for scene enrichment

## Project Structure

```text
geosim-futo/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── outputs/
└── app/
