"""
simulation.py
-------------
Flood susceptibility mapping, risk classification, inundation scenario
modelling, and semantic scene-zone derivation.

Notebook source: Cells 23–51
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Flood susceptibility
# ---------------------------------------------------------------------------

def compute_flood_susceptibility(
    idw_surface: np.ndarray,
    slope_degrees: np.ndarray,
    terrain_class: np.ndarray,
    weight_elevation: float = 0.45,
    weight_slope: float = 0.35,
    weight_terrain: float = 0.20,
) -> np.ndarray:
    """
    Derive a continuous flood susceptibility index via weighted overlay.

    Each factor is normalised to [0, 1] before weighting:

    * **Elevation vulnerability** — lower elevation → higher score
      ``1 - (elev - elev_min) / (elev_max - elev_min)``
    * **Slope vulnerability** — flatter slope → higher score
      ``1 - (slope - slope_min) / (slope_max - slope_min)``
    * **Terrain class vulnerability** — fixed class scores:
      Lowland = 1.0, Midland = 0.5, Highland = 0.1

    Parameters
    ----------
    idw_surface : np.ndarray
        Elevation grid (metres).
    slope_degrees : np.ndarray
        Slope grid (degrees).
    terrain_class : np.ndarray
        Terrain class grid (1=Lowland, 2=Midland, 3=Highland).
    weight_elevation : float, optional
        Weight for the elevation factor (default 0.45).
    weight_slope : float, optional
        Weight for the slope factor (default 0.35).
    weight_terrain : float, optional
        Weight for the terrain-class factor (default 0.20).

    Returns
    -------
    np.ndarray
        Flood susceptibility index (continuous, same shape as inputs).
    """
    # Elevation vulnerability (lower = more at risk)
    elev_min = float(np.min(idw_surface))
    elev_max = float(np.max(idw_surface))
    elevation_vulnerability = 1.0 - ((idw_surface - elev_min) / (elev_max - elev_min))

    # Slope vulnerability (flatter = more at risk)
    slope_min = float(np.min(slope_degrees))
    slope_max = float(np.max(slope_degrees))
    slope_vulnerability = 1.0 - ((slope_degrees - slope_min) / (slope_max - slope_min))

    # Terrain class vulnerability (discrete look-up)
    terrain_vulnerability = np.zeros_like(terrain_class, dtype=float)
    terrain_vulnerability[terrain_class == 1] = 1.0   # Lowland  — highest risk
    terrain_vulnerability[terrain_class == 2] = 0.5   # Midland  — moderate risk
    terrain_vulnerability[terrain_class == 3] = 0.1   # Highland — lowest risk

    flood_susceptibility = (
        weight_elevation * elevation_vulnerability
        + weight_slope   * slope_vulnerability
        + weight_terrain * terrain_vulnerability
    )

    return flood_susceptibility


def classify_flood_risk(
    flood_susceptibility: np.ndarray,
    low_percentile: float = 33,
    high_percentile: float = 66,
) -> tuple[np.ndarray, float, float]:
    """
    Classify continuous flood susceptibility into three risk zones.

    Classes
    -------
    1 = Low risk
    2 = Moderate risk
    3 = High risk

    Parameters
    ----------
    flood_susceptibility : np.ndarray
        Continuous susceptibility surface.
    low_percentile : float, optional
        Percentile separating Low from Moderate risk (default 33).
    high_percentile : float, optional
        Percentile separating Moderate from High risk (default 66).

    Returns
    -------
    risk_class : np.ndarray
        Integer class array (1, 2, 3).
    low_threshold : float
        Susceptibility value at *low_percentile*.
    high_threshold : float
        Susceptibility value at *high_percentile*.
    """
    low_threshold  = float(np.percentile(flood_susceptibility, low_percentile))
    high_threshold = float(np.percentile(flood_susceptibility, high_percentile))

    risk_class = np.zeros_like(flood_susceptibility)
    risk_class[flood_susceptibility <= low_threshold]                                              = 1
    risk_class[(flood_susceptibility > low_threshold) & (flood_susceptibility <= high_threshold)] = 2
    risk_class[flood_susceptibility > high_threshold]                                              = 3

    # Print zone summary (mirrors notebook Cell 30)
    unique, counts = np.unique(risk_class, return_counts=True)
    labels = {1: "Low", 2: "Moderate", 3: "High"}
    for u, c in zip(unique, counts):
        print(f"{labels[int(u)]} susceptibility: {c} grid cells")

    return risk_class, low_threshold, high_threshold


# ---------------------------------------------------------------------------
# Inundation scenarios
# ---------------------------------------------------------------------------

def build_inundation_scenarios(
    idw_surface: np.ndarray,
) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    """
    Simulate three progressive inundation scenarios from the IDW surface.

    Water-level thresholds are derived from elevation percentiles
    (25th, 40th, 55th), matching notebook Cells 40–44.

    Parameters
    ----------
    idw_surface : np.ndarray
        IDW elevation surface (metres).

    Returns
    -------
    summary_df : pd.DataFrame
        Columns: ``scenario``, ``water_level_m``, ``inundated_cells``,
        ``inundated_percent``.
    masks : dict[str, np.ndarray of bool]
        Keys: ``"Mild"``, ``"Moderate"``, ``"Severe"``.
        Each mask is ``True`` where the cell is inundated.
    """
    mild_level     = float(np.percentile(idw_surface, 25))
    moderate_level = float(np.percentile(idw_surface, 40))
    severe_level   = float(np.percentile(idw_surface, 55))

    print(f"Mild scenario water level:     {mild_level:.4f} m")
    print(f"Moderate scenario water level: {moderate_level:.4f} m")
    print(f"Severe scenario water level:   {severe_level:.4f} m")

    mild_mask     = idw_surface <= mild_level
    moderate_mask = idw_surface <= moderate_level
    severe_mask   = idw_surface <= severe_level

    total_cells = idw_surface.size

    summary_df = pd.DataFrame({
        "scenario":         ["Mild",       "Moderate",       "Severe"],
        "water_level_m":    [mild_level,   moderate_level,   severe_level],
        "inundated_cells":  [int(np.sum(mild_mask)), int(np.sum(moderate_mask)), int(np.sum(severe_mask))],
        "inundated_percent": [
            100.0 * np.sum(mild_mask)     / total_cells,
            100.0 * np.sum(moderate_mask) / total_cells,
            100.0 * np.sum(severe_mask)   / total_cells,
        ],
    })

    masks = {
        "Mild":     mild_mask,
        "Moderate": moderate_mask,
        "Severe":   severe_mask,
    }

    return summary_df, masks


# ---------------------------------------------------------------------------
# Semantic scene zones
# ---------------------------------------------------------------------------

def build_scene_zones(
    terrain_class: np.ndarray,
    risk_class: np.ndarray,
) -> np.ndarray:
    """
    Combine terrain class and flood risk into four semantic scene zones.

    Zone definitions (notebook Cell 49)
    ------------------------------------
    1 = Wet Lowland        — Lowland + High or Moderate flood risk
    2 = Transitional Midland — all Midland cells
    3 = Stable Upland      — Highland + Low flood risk
    4 = Mixed Terrain      — all remaining cells

    Parameters
    ----------
    terrain_class : np.ndarray
        Terrain class grid (1, 2, 3).
    risk_class : np.ndarray
        Flood risk class grid (1, 2, 3).

    Returns
    -------
    np.ndarray
        Scene zone grid (integer values 1–4), same shape as inputs.
    """
    scene_zone = np.zeros_like(terrain_class)

    scene_zone[(terrain_class == 1) & (risk_class >= 2)] = 1   # Wet Lowland
    scene_zone[(terrain_class == 2)]                      = 2   # Transitional Midland
    scene_zone[(terrain_class == 3) & (risk_class == 1)] = 3   # Stable Upland
    scene_zone[scene_zone == 0]                           = 4   # Mixed Terrain

    return scene_zone


def compute_zone_stats(scene_zone: np.ndarray) -> pd.DataFrame:
    """
    Return a DataFrame summarising the cell count and percentage for each
    semantic scene zone.

    Parameters
    ----------
    scene_zone : np.ndarray
        Output of :func:`build_scene_zones`.

    Returns
    -------
    pd.DataFrame
        Columns: ``zone_value``, ``zone_name``, ``cell_count``, ``percent``.
    """
    zone_labels = {
        1: "Wet Lowland",
        2: "Transitional Midland",
        3: "Stable Upland",
        4: "Mixed Terrain",
    }
    total_cells = scene_zone.size

    rows = []
    for zone_value, zone_name in zone_labels.items():
        count = int(np.sum(scene_zone == zone_value))
        rows.append({
            "zone_value": zone_value,
            "zone_name":  zone_name,
            "cell_count": count,
            "percent":    100.0 * count / total_cells,
        })

    return pd.DataFrame(rows)
