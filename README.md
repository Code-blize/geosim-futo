# GeoSim FUTO

**Terrain Interpolation & Environmental Change Simulation**  
*Federal University of Technology Owerri (FUTO), Imo State, Nigeria*

---

## Overview

GeoSim FUTO reconstructs a continuous terrain surface from 11 sparse ground-based elevation
survey points collected across the FUTO campus and five surrounding communities. It applies
spatial interpolation, slope analysis, terrain classification, flood susceptibility mapping,
and scenario-based inundation modelling — then bridges those GIS outputs into structured
**Generative AI scene prompts** for immersive AR/VR environmental visualisation.

The project demonstrates how real geospatial data, environmental analysis, and Generative AI
can be combined into a single reproducible spatial workflow.

---

## Project Structure

```
geosim-futo/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
│
├── data/
│   ├── raw/
│   │   └── futo_elevation_points.csv           # 11 VES survey stations
│   └── processed/
│       ├── interpolation_validation_results.csv
│       ├── futo_terrain_grid.csv               # IDW surface (150 × 150 grid)
│       ├── terrain_class_grid.csv              # Lowland / Midland / Highland
│       ├── flood_susceptibility_grid.csv       # Risk index + classified zone
│       └── scenario_summary.csv               # Mild / Moderate / Severe stats
│
├── notebooks/
│   ├── 01_data_loading_and_cleaning.ipynb
│   ├── 02_interpolation_comparison_and_validation.ipynb
│   ├── 03_terrain_analysis.ipynb
│   ├── 04_flood_susceptibility_mapping.ipynb
│   ├── 05_scenario_simulation.ipynb
│   └── 06_genai_scene_pipeline.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_processing.py     # Dataset loading and grid creation
│   ├── interpolation.py       # IDW + griddata methods + LOO cross-validation
│   ├── terrain_analysis.py    # Slope computation and terrain classification
│   ├── susceptibility.py      # Flood susceptibility weighted overlay
│   ├── simulation.py          # Inundation scenarios and semantic scene zones
│   ├── genai_pipeline.py      # AI scene prompts, project narrative, abstract
│   └── visualization.py       # Static (Matplotlib) and interactive (Plotly) plots
│
├── outputs/
│   ├── figures/               # 9 exported PNG maps
│   ├── reports/               # Narrative, abstract, scene prompts (.txt)
│   └── tables/                # zone_stats.csv, project_metrics.json, scene_prompts.json
│
├── app/
│   └── web/                   # 3 interactive Plotly HTML visualisations
│
└── docs/
    ├── methodology.md
    ├── results_summary.md
    └── project_scope.md
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/geosim-futo.git
cd geosim-futo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the notebooks in order

```bash
jupyter notebook notebooks/
```

Open and run notebooks `01` through `06` in sequence.

### 4. Or use the src modules directly

```python
import sys
sys.path.insert(0, 'src')

from data_processing import load_survey_data, prepare_grid
from interpolation import run_all_interpolations
from terrain_analysis import compute_slope, classify_terrain
from susceptibility import compute_flood_susceptibility, classify_flood_risk
from simulation import build_inundation_scenarios, build_scene_zones
from genai_pipeline import build_all_scene_prompts

# Load the 11-point survey dataset and build a 150×150 interpolation grid
df = load_survey_data()
x, y, z = df['longitude'].values, df['latitude'].values, df['elevation_m'].values
grid_x, grid_y = prepare_grid(x, y)

# Run all four interpolation methods; IDW is selected downstream
surfaces = run_all_interpolations(x, y, z, grid_x, grid_y)
idw_surface = surfaces['IDW']

# Terrain → flood susceptibility → scenarios
slope_degrees, _, _ = compute_slope(idw_surface, grid_x, grid_y)
terrain_class, _, _ = classify_terrain(idw_surface)
flood_susceptibility = compute_flood_susceptibility(idw_surface, slope_degrees, terrain_class)
risk_class, _, _ = classify_flood_risk(flood_susceptibility)
summary_df, masks = build_inundation_scenarios(idw_surface)
```

---

## Methodology Summary

### 1 · Spatial Interpolation
Four methods were implemented and evaluated on the 11 survey points using **leave-one-out
cross-validation**:

| Method | RMSE (m) | Valid Predictions |
|---|---|---|
| Nearest Neighbour | 23.86 | 11 / 11 |
| Linear (Delaunay) | 15.59 | 7 / 11 |
| Cubic Spline | 14.58 | 7 / 11 |
| **IDW** *(selected)* | **20.94** | **11 / 11** |

**IDW was selected** because it is the only method achieving complete spatial coverage
(11 / 11 valid predictions). Cubic and Linear had lower RMSE but failed to predict 4 out of
11 held-out points due to the sparse, non-uniform distribution of the survey network.

### 2 · Terrain Analysis
- **Slope** computed via `numpy.gradient` with degree-to-metre conversion
- **Terrain classification** split at the 33rd and 66th elevation percentiles:
  Lowland (≤ 189.7 m), Midland (189.7–198.1 m), Highland (> 198.1 m)

### 3 · Flood Susceptibility
Weighted overlay of three normalised vulnerability factors:

```
Flood Susceptibility = 0.45 × elevation_vuln
                     + 0.35 × slope_vuln
                     + 0.20 × terrain_class_vuln
```

### 4 · Inundation Scenarios
Water-level thresholds derived from IDW surface percentiles:

| Scenario | Water Level (m) | Area Flooded |
|---|---|---|
| Mild | 186.37 | 25% |
| Moderate | 192.09 | 40% |
| Severe | 195.98 | 55% |

### 5 · Generative AI Pipeline
GIS-derived metrics, zone statistics, and scenario outputs are encoded into structured prompts
for AR/VR-ready 3D scene generation — one prompt per inundation scenario.

---

## Key Results

| Metric | Value |
|---|---|
| Interpolation method selected | IDW (power = 2) |
| Elevation range | 159 m – 229 m |
| Mean elevation | 193.37 m |
| Mean slope | 0.35° |
| Dominant terrain class | Highland |
| High flood risk coverage | 34% of study area |
| Moderate scenario inundation | 40% at water level 192.09 m |

---

## Outputs

| Type | Location | Count |
|---|---|---|
| PNG maps | `outputs/figures/` | 9 |
| Interactive HTML | `app/web/` | 3 |
| Text reports | `outputs/reports/` | 3 |
| CSV / JSON tables | `outputs/tables/` | 3 |
| Processed data CSVs | `data/processed/` | 5 |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| NumPy | Grid computation and array operations |
| Pandas | Tabular data management |
| SciPy | Linear, Cubic, and Nearest interpolation |
| Matplotlib | All static map outputs |
| Plotly | Interactive 3D visualisations |
| Jupyter | Notebook-based workflow |

---

## Documentation

- [Methodology](docs/methodology.md) — Step-by-step technical approach
- [Results Summary](docs/results_summary.md) — Key findings and full output inventory
- [Project Scope](docs/project_scope.md) — Objectives, deliverables, and limitations

---

## License

MIT License — see [LICENSE](LICENSE) for details.
