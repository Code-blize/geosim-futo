# GeoSim FUTO

**GeoSim FUTO** is a Generative AI-enhanced GIS project for 3D terrain reconstruction, environmental vulnerability mapping, and scenario-based inundation simulation around the Federal University of Technology Owerri (FUTO), Nigeria.

The project combines geospatial interpolation, terrain analysis, weighted flood susceptibility modeling, interactive 3D visualization, and data-grounded Generative AI scene prompting in a single end-to-end workflow.

---

## Overview

This project was developed as a learning-driven GIS and data science workflow using real elevation point data from locations around FUTO and nearby communities. The study reconstructs terrain from sparse sampled points, analyzes surface characteristics, identifies environmentally vulnerable zones, simulates inundation scenarios, and translates GIS outputs into immersive scene prompts for future AR/VR-style visualization.

Rather than using Generative AI to invent terrain, the project uses real GIS-derived terrain and environmental metrics as the foundation, while Generative AI is applied as a grounded scene-generation and storytelling layer.

---

## Project Aim

To develop a GIS-based environmental modeling workflow that reconstructs terrain from real elevation points, identifies flood-prone zones, simulates environmental change, and integrates Generative AI for immersive geospatial visualization.

---

## Objectives

- Organize and analyze real-world elevation point data around FUTO
- Compare interpolation methods for terrain reconstruction
- Select the most suitable interpolation method using validation
- Derive terrain products such as contours, slope, and terrain classes
- Build a flood susceptibility model using weighted overlay
- Simulate mild, moderate, and severe inundation scenarios
- Create interactive 3D terrain and environmental risk visualizations
- Generate data-grounded AI prompts for immersive environmental scene design

---

## Study Area

The study area covers locations around the Federal University of Technology Owerri (FUTO), including surrounding communities such as Eziobodo, Obinze, Avu, Nekede, and Ihiagwa in Imo State, Nigeria.

---

## Dataset

The project uses sparse elevation survey points with the following attributes:

- Point ID
- Longitude
- Latitude
- Elevation (m)
- Location name

These measured points were used as the basis for terrain interpolation and subsequent environmental analysis.

---

## Methodology

The workflow followed these major stages:

1. **Data loading and cleaning**  
   Elevation point data was structured into a clean tabular format.

2. **Interpolation comparison and validation**  
   Four interpolation methods were compared:
   - Nearest Neighbor
   - Linear
   - Cubic
   - Inverse Distance Weighting (IDW)

   Leave-One-Out Cross-Validation (LOOCV) was used to assess prediction reliability. IDW was selected as the most practical method because it provided complete prediction coverage and stable performance for the sparse dataset.

3. **Terrain analysis**  
   The selected IDW surface was used to generate:
   - Contour map
   - Slope map
   - Terrain classification map

4. **Flood susceptibility mapping**  
   A weighted overlay approach combined:
   - Elevation vulnerability
   - Slope vulnerability
   - Terrain-class vulnerability

   This produced both continuous and classified flood susceptibility layers.

5. **Scenario-based environmental simulation**  
   Mild, moderate, and severe inundation scenarios were created using terrain-based water-level thresholds to simulate how increasing inundation could affect the study area.

6. **Interactive 3D visualization**  
   Plotly was used to create interactive browser-based 3D terrain and flood-risk scenes.

7. **Generative AI integration**  
   GIS-derived environmental outputs were translated into:
   - Semantic scene zones
   - Data-grounded AI scene prompts
   - Narrative summaries for communication and immersive visualization planning

---

## Key Results

The project produced:

- Interpolation comparison in 2D and 3D
- Validation table for interpolation method selection
- IDW-based terrain surface
- Contour map
- Slope map
- Terrain classification map
- Flood susceptibility map
- Classified flood susceptibility zones
- Scenario-based inundation simulation
- Interactive 3D terrain and flood-risk HTML outputs
- Semantic scene zoning for generative visualization
- Data-grounded Generative AI prompts
- Project narrative and abstract

---

## Generative AI Layer

The Generative AI component of this project does not replace GIS analysis. Instead, it uses GIS-derived terrain, scene zoning, susceptibility patterns, and scenario metrics to generate grounded prompts for immersive environmental visualization.

This makes the AI layer:
- evidence-based
- geographically informed
- suitable for future AR/VR-style applications
- useful for environmental storytelling and presentation

---

## Project Structure

```text
geosim-futo/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   │   └── futo_elevation_points.csv
│   └── processed/
├── notebooks/
│   └── 00_geosim_futo_full_workflow.ipynb
├── src/
├── outputs/
│   ├── figures/
│   ├── reports/
│   └── tables/
├── app/
│   └── web/
└── docs/
