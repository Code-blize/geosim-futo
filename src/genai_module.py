"""
genai_module.py
---------------
Generates data-grounded Generative AI scene prompts and project narrative
text from GIS-derived terrain metrics, zone statistics, and inundation
scenario outputs.

Notebook source: Cells 52–64
"""

import pandas as pd


# ---------------------------------------------------------------------------
# Scene prompt builder
# ---------------------------------------------------------------------------

def build_scene_prompt(
    scenario_name: str,
    water_level: float,
    inundated_percent: float,
    metrics: dict,
    zone_stats_df: pd.DataFrame,
) -> str:
    """
    Build a structured Generative AI prompt for a single inundation scenario.

    The prompt encodes real GIS-derived values (elevation range, dominant
    terrain, flood risk coverage, etc.) so that an image/3D generation model
    can produce a geospatially grounded AR/VR scene.

    Parameters
    ----------
    scenario_name : str
        Human-readable scenario label, e.g. ``"Mild"``.
    water_level : float
        Water-level threshold for this scenario (metres).
    inundated_percent : float
        Percentage of the study area that is inundated under this scenario.
    metrics : dict
        Project-level metrics from
        :func:`terrain_analysis.compute_project_metrics`.
    zone_stats_df : pd.DataFrame
        Zone statistics from :func:`simulation.compute_zone_stats`.

    Returns
    -------
    str
        Ready-to-use prompt string (stripped of leading/trailing whitespace).
    """
    dominant_zone = (
        zone_stats_df
        .sort_values("percent", ascending=False)
        .iloc[0]["zone_name"]
    )

    prompt = f"""
Create an immersive 3D geospatial scene of the FUTO study area in Nigeria.

Base terrain requirements:
- Use a real terrain surface reconstructed from sparse elevation survey points
- Interpolation method used: IDW
- Elevation range: {metrics['elevation_min']:.2f} m to {metrics['elevation_max']:.2f} m
- Mean elevation: {metrics['mean_elevation']:.2f} m
- Dominant terrain type: {metrics['dominant_terrain']}
- Mean slope: {metrics['mean_slope']:.2f} degrees

Environmental interpretation:
- Dominant scene zone: {dominant_zone}
- High-risk flood susceptibility zone coverage: {metrics['high_risk_percent']:.2f}%
- Moderate-risk flood susceptibility zone coverage: {metrics['moderate_risk_percent']:.2f}%
- Low-risk flood susceptibility zone coverage: {metrics['low_risk_percent']:.2f}%

Scenario to visualize:
- Scenario name: {scenario_name}
- Water level threshold: {water_level:.2f} m
- Inundated terrain proportion: {inundated_percent:.2f}%

Visual design instructions:
- Preserve real topography and terrain gradients
- Show inundated areas as realistic low-lying water-covered zones
- Represent wet lowlands with waterlogged surfaces and dense moisture-loving vegetation
- Represent transitional midlands with mixed vegetation and moderate dryness
- Represent stable uplands with firmer ground and reduced water presence
- Keep the environment educational, analytical, and geospatially realistic
- Avoid fantasy elements
- Make the scene suitable for an AR/VR environmental simulation concept

Output goal:
Generate a realistic environmental visualization concept grounded in GIS-derived terrain and flood susceptibility patterns.
""".strip()

    return prompt


def build_all_scene_prompts(
    summary_df: pd.DataFrame,
    metrics: dict,
    zone_stats_df: pd.DataFrame,
    save_path: str | None = "futo_genai_scene_prompts.txt",
    verbose: bool = True,
) -> dict[str, str]:
    """
    Build scene prompts for all inundation scenarios in *summary_df*.

    Optionally saves them to a text file and prints a preview.

    Parameters
    ----------
    summary_df : pd.DataFrame
        Output of :func:`simulation.build_inundation_scenarios`
        (columns: ``scenario``, ``water_level_m``, ``inundated_percent``).
    metrics : dict
        Project metrics from :func:`terrain_analysis.compute_project_metrics`.
    zone_stats_df : pd.DataFrame
        Zone statistics from :func:`simulation.compute_zone_stats`.
    save_path : str or None, optional
        File path to write the prompts (default
        ``"futo_genai_scene_prompts.txt"``).  Pass ``None`` to skip saving.
    verbose : bool, optional
        If ``True``, print a 1200-character preview of each prompt.

    Returns
    -------
    dict[str, str]
        Mapping of scenario name → prompt string.
    """
    scene_prompts: dict[str, str] = {}

    for _, row in summary_df.iterrows():
        prompt = build_scene_prompt(
            scenario_name=row["scenario"],
            water_level=row["water_level_m"],
            inundated_percent=row["inundated_percent"],
            metrics=metrics,
            zone_stats_df=zone_stats_df,
        )
        scene_prompts[row["scenario"]] = prompt

    if verbose:
        for name, prompt in scene_prompts.items():
            print(f"\n{'=' * 60}")
            print(f"{name.upper()} SCENARIO PROMPT")
            print(f"{'=' * 60}\n")
            print(prompt[:1200], "...\n")

    if save_path is not None:
        with open(save_path, "w", encoding="utf-8") as f:
            for name, prompt in scene_prompts.items():
                f.write(f"{'=' * 70}\n")
                f.write(f"{name.upper()} SCENARIO PROMPT\n")
                f.write(f"{'=' * 70}\n")
                f.write(prompt)
                f.write("\n\n")
        print(f"Saved as {save_path}")

    return scene_prompts


# ---------------------------------------------------------------------------
# Narrative & abstract builders
# ---------------------------------------------------------------------------

def build_project_narrative(
    project_metrics: dict,
    zone_stats_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    save_path: str | None = "futo_project_narrative.txt",
) -> str:
    """
    Generate a plain-English project narrative from GIS-derived outputs.

    The narrative describes the interpolation method, terrain
    characteristics, flood susceptibility findings, inundation scenario
    results, and the Generative AI bridge — ready for a README, report,
    or StoryMap.

    Parameters
    ----------
    project_metrics : dict
        From :func:`terrain_analysis.compute_project_metrics`.
    zone_stats_df : pd.DataFrame
        From :func:`simulation.compute_zone_stats`.
    summary_df : pd.DataFrame
        From :func:`simulation.build_inundation_scenarios`.
    save_path : str or None, optional
        File path to write the narrative (default
        ``"futo_project_narrative.txt"``).  Pass ``None`` to skip.

    Returns
    -------
    str
        Narrative text (stripped).
    """
    dominant_zone = (
        zone_stats_df
        .sort_values("percent", ascending=False)
        .iloc[0]["zone_name"]
    )

    mild_pct     = summary_df.loc[summary_df["scenario"] == "Mild",     "inundated_percent"].values[0]
    moderate_pct = summary_df.loc[summary_df["scenario"] == "Moderate", "inundated_percent"].values[0]
    severe_pct   = summary_df.loc[summary_df["scenario"] == "Severe",   "inundated_percent"].values[0]

    narrative = f"""
GeoSim FUTO is a geospatial data science project that reconstructs terrain around the Federal University of Technology Owerri (FUTO) using sparse elevation survey points and applies environmental screening methods to simulate landscape vulnerability.

The terrain surface was generated using Inverse Distance Weighting (IDW), selected as the most practical interpolation method because it provided complete spatial coverage during validation while maintaining a realistic terrain form for the available dataset. The reconstructed surface spans an elevation range of {project_metrics['elevation_min']:.2f} m to {project_metrics['elevation_max']:.2f} m, with a mean elevation of {project_metrics['mean_elevation']:.2f} m.

Terrain analysis showed that the area contains a mix of lowland, midland, and highland characteristics, while semantic scene zoning identified {dominant_zone} as the dominant environmental scene type. The average slope of the reconstructed terrain was {project_metrics['mean_slope']:.2f} degrees, indicating generally gentle terrain with a few localized areas of stronger elevation change.

A weighted overlay model combining elevation, slope, and terrain class was used to derive flood susceptibility. To explore environmental change, terrain-based inundation scenarios were simulated. Under the mild scenario, approximately {mild_pct:.2f}% of the terrain was affected. This increased to {moderate_pct:.2f}% under the moderate scenario and {severe_pct:.2f}% under the severe scenario, showing how progressively higher water levels could affect broader portions of the landscape.

The Generative AI component of the project does not replace GIS analysis. Instead, it uses GIS-derived terrain metrics, environmental zones, and scenario outputs to generate grounded prompts for immersive 3D environmental visualization. This creates a bridge between spatial analysis and future AR/VR-ready scene generation.

Overall, the project demonstrates how real geospatial data, terrain analysis, environmental simulation, and Generative AI can be combined into a single workflow for interactive and educational environmental visualization.
""".strip()

    if save_path is not None:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(narrative)
        print(f"Saved as {save_path}")

    return narrative


def build_project_abstract(
    project_metrics: dict | None = None,
    save_path: str | None = "futo_project_abstract.txt",
) -> str:
    """
    Return the fixed project abstract (as written in the notebook Cell 61).

    Parameters
    ----------
    project_metrics : dict or None
        Unused — kept for API symmetry.  The abstract is a static string.
    save_path : str or None, optional
        File path to write the abstract.  Pass ``None`` to skip.

    Returns
    -------
    str
        Abstract text (stripped).
    """
    abstract = (
        "This project presents a Generative AI-enhanced GIS workflow for 3D terrain "
        "reconstruction and environmental change simulation around the Federal University "
        "of Technology Owerri (FUTO), Nigeria. Sparse elevation survey points were "
        "interpolated into a continuous terrain surface using Inverse Distance Weighting "
        "(IDW), selected for its complete spatial coverage and stable validation "
        "performance. Derived terrain products included contour mapping, slope analysis, "
        "terrain classification, and flood susceptibility mapping through weighted "
        "overlay. Scenario-based inundation modeling showed progressive terrain exposure "
        "under increasing water-level thresholds. To support immersive visualization, "
        "GIS-derived terrain metrics and environmental zones were translated into "
        "data-grounded Generative AI prompts for future AR/VR-style scene generation. "
        "The project demonstrates the integration of GIS, environmental modeling, and "
        "Generative AI within a reproducible spatial analysis framework."
    )

    if save_path is not None:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(abstract)
        print(f"Saved as {save_path}")

    return abstract
