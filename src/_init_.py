# GeoSim FUTO
# Terrain Interpolation & Environmental Change Simulation
# Federal University of Technology Owerri (FUTO), Nigeria

from .data_processing import load_survey_data, prepare_grid
from .interpolation import (
    idw_interpolation,
    run_all_interpolations,
    predict_idw,
    predict_griddata,
    run_leave_one_out_validation,
    select_best_method,
)
from .terrain_analysis import (
    compute_slope,
    classify_terrain,
    summarise_terrain_classes,
    compute_project_metrics,
)
from .simulation import (
    compute_flood_susceptibility,
    classify_flood_risk,
    build_inundation_scenarios,
    build_scene_zones,
    compute_zone_stats,
)
from .genai_module import build_scene_prompt, build_all_scene_prompts, build_project_narrative
from .visualization import (
    plot_interpolation_comparison,
    plot_3d_surfaces,
    plot_idw_contour,
    plot_slope_map,
    plot_terrain_classification,
    plot_flood_susceptibility,
    plot_classified_flood_risk,
    plot_inundation_scenarios,
    plot_inundation_bar,
    plot_scene_zones,
    plot_interactive_terrain,
    plot_interactive_flood_susceptibility,
    plot_interactive_inundation_scenario,
)
from .utils import (
    compute_grid_spacing_metres,
    normalise_array,
    percentile_thresholds,
    print_section,
    save_text_output,
)

__all__ = [
    "load_survey_data",
    "prepare_grid",
    "idw_interpolation",
    "run_all_interpolations",
    "predict_idw",
    "predict_griddata",
    "run_leave_one_out_validation",
    "select_best_method",
    "compute_slope",
    "classify_terrain",
    "summarise_terrain_classes",
    "compute_project_metrics",
    "compute_flood_susceptibility",
    "classify_flood_risk",
    "build_inundation_scenarios",
    "build_scene_zones",
    "compute_zone_stats",
    "build_scene_prompt",
    "build_all_scene_prompts",
    "build_project_narrative",
    "plot_interpolation_comparison",
    "plot_3d_surfaces",
    "plot_idw_contour",
    "plot_slope_map",
    "plot_terrain_classification",
    "plot_flood_susceptibility",
    "plot_classified_flood_risk",
    "plot_inundation_scenarios",
    "plot_inundation_bar",
    "plot_scene_zones",
    "plot_interactive_terrain",
    "plot_interactive_flood_susceptibility",
    "plot_interactive_inundation_scenario",
    "compute_grid_spacing_metres",
    "normalise_array",
    "percentile_thresholds",
    "print_section",
    "save_text_output",
]
