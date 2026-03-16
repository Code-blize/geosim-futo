"""
terrain_analysis.py
-------------------
Derives secondary terrain products from the IDW elevation surface:
slope, terrain classification, and project-level summary metrics.

Notebook source: Cells 16–22, 52
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Slope
# ---------------------------------------------------------------------------

def compute_slope(
    idw_surface: np.ndarray,
    grid_x: np.ndarray,
    grid_y: np.ndarray,
) -> tuple[np.ndarray, float, float]:
    """
    Compute slope in degrees from an IDW elevation surface.

    Grid spacing is converted from decimal degrees to metres using
    latitude-aware scale factors (same approach as notebook Cell 16).

    Parameters
    ----------
    idw_surface : np.ndarray, shape (rows, cols)
        Interpolated elevation grid (metres).
    grid_x : np.ndarray, shape (rows, cols)
        Longitude coordinates of the grid.
    grid_y : np.ndarray, shape (rows, cols)
        Latitude coordinates of the grid.

    Returns
    -------
    slope_degrees : np.ndarray, shape (rows, cols)
        Slope at each grid node in degrees.
    dx_m : float
        Grid spacing in the x-direction (metres).
    dy_m : float
        Grid spacing in the y-direction (metres).

    Notes
    -----
    The slope is computed as
    ``arctan(sqrt((dz/dx)^2 + (dz/dy)^2))``
    where gradients are calculated with :func:`numpy.gradient`.
    """
    mean_lat = float(np.mean(grid_y))

    # Degree-to-metre conversion factors
    meters_per_degree_lat = 111_320.0
    meters_per_degree_lon = 111_320.0 * np.cos(np.radians(mean_lat))

    dx_deg = float(grid_x[1, 0] - grid_x[0, 0])
    dy_deg = float(grid_y[0, 1] - grid_y[0, 0])

    dx_m = dx_deg * meters_per_degree_lon
    dy_m = dy_deg * meters_per_degree_lat

    print(f"Approximate grid spacing in x (meters): {dx_m:.4f}")
    print(f"Approximate grid spacing in y (meters): {dy_m:.4f}")

    dz_dx, dz_dy = np.gradient(idw_surface, dx_m, dy_m)

    slope_radians = np.arctan(np.sqrt(dz_dx ** 2 + dz_dy ** 2))
    slope_degrees = np.degrees(slope_radians)

    return slope_degrees, dx_m, dy_m


# ---------------------------------------------------------------------------
# Terrain classification
# ---------------------------------------------------------------------------

def classify_terrain(
    idw_surface: np.ndarray,
    low_percentile: float = 33,
    high_percentile: float = 66,
) -> tuple[np.ndarray, float, float]:
    """
    Classify the elevation surface into three terrain classes.

    Classes
    -------
    1 = Lowland   (elevation ≤ low_threshold)
    2 = Midland   (low_threshold < elevation ≤ high_threshold)
    3 = Highland  (elevation > high_threshold)

    Parameters
    ----------
    idw_surface : np.ndarray
        Interpolated elevation grid (metres).
    low_percentile : float, optional
        Percentile defining the Lowland / Midland boundary (default 33).
    high_percentile : float, optional
        Percentile defining the Midland / Highland boundary (default 66).

    Returns
    -------
    terrain_class : np.ndarray, same shape as *idw_surface*
        Integer class array (values 1, 2, 3).
    low_threshold : float
        Elevation threshold between Lowland and Midland (metres).
    high_threshold : float
        Elevation threshold between Midland and Highland (metres).
    """
    low_threshold  = float(np.percentile(idw_surface, low_percentile))
    high_threshold = float(np.percentile(idw_surface, high_percentile))

    print(f"Lowland threshold:  {low_threshold:.4f} m")
    print(f"Highland threshold: {high_threshold:.4f} m")

    terrain_class = np.zeros_like(idw_surface)
    terrain_class[idw_surface <= low_threshold]                                        = 1
    terrain_class[(idw_surface > low_threshold) & (idw_surface <= high_threshold)]    = 2
    terrain_class[idw_surface > high_threshold]                                        = 3

    return terrain_class, low_threshold, high_threshold


def summarise_terrain_classes(terrain_class: np.ndarray) -> None:
    """
    Print the number of grid cells in each terrain class.

    Parameters
    ----------
    terrain_class : np.ndarray
        Output of :func:`classify_terrain`.
    """
    labels = {1: "Lowland", 2: "Midland", 3: "Highland"}
    unique, counts = np.unique(terrain_class, return_counts=True)

    for u, c in zip(unique, counts):
        label = labels.get(int(u), str(int(u)))
        print(f"{label}: {c} grid cells")


# ---------------------------------------------------------------------------
# Project-level metrics
# ---------------------------------------------------------------------------

def compute_project_metrics(
    idw_surface: np.ndarray,
    slope_degrees: np.ndarray,
    terrain_class: np.ndarray,
    risk_class: np.ndarray,
) -> dict:
    """
    Compute a dictionary of high-level project summary metrics.

    Parameters
    ----------
    idw_surface : np.ndarray
        IDW elevation grid (metres).
    slope_degrees : np.ndarray
        Slope grid in degrees (from :func:`compute_slope`).
    terrain_class : np.ndarray
        Terrain class grid (1=Lowland, 2=Midland, 3=Highland).
    risk_class : np.ndarray
        Flood risk class grid (1=Low, 2=Moderate, 3=High).

    Returns
    -------
    dict
        Keys: ``elevation_min``, ``elevation_max``, ``mean_elevation``,
        ``mean_slope``, ``max_slope``, ``dominant_terrain``,
        ``high_risk_percent``, ``moderate_risk_percent``,
        ``low_risk_percent``.
    """
    terrain_labels = {1: "Lowland", 2: "Midland", 3: "Highland"}
    terrain_counts = {
        label: int(np.sum(terrain_class == key))
        for key, label in terrain_labels.items()
    }
    dominant_terrain = max(terrain_counts, key=terrain_counts.get)

    metrics = {
        "elevation_min":        float(np.min(idw_surface)),
        "elevation_max":        float(np.max(idw_surface)),
        "mean_elevation":       float(np.mean(idw_surface)),
        "mean_slope":           float(np.mean(slope_degrees)),
        "max_slope":            float(np.max(slope_degrees)),
        "dominant_terrain":     dominant_terrain,
        "high_risk_percent":    float(100 * np.sum(risk_class == 3) / risk_class.size),
        "moderate_risk_percent":float(100 * np.sum(risk_class == 2) / risk_class.size),
        "low_risk_percent":     float(100 * np.sum(risk_class == 1) / risk_class.size),
    }

    return metrics
