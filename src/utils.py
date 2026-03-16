"""
utils.py
--------
Shared helper utilities used across the GeoSim FUTO modules.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Numeric helpers
# ---------------------------------------------------------------------------

def compute_grid_spacing_metres(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
) -> tuple[float, float]:
    """
    Estimate physical grid spacing (in metres) from a degree-based meshgrid.

    Uses the mean latitude of the grid to compute an approximate longitude
    scaling factor, matching the approach in notebook Cell 16.

    Parameters
    ----------
    grid_x : np.ndarray, shape (rows, cols)
        Longitude meshgrid.
    grid_y : np.ndarray, shape (rows, cols)
        Latitude meshgrid.

    Returns
    -------
    dx_m : float
        Grid spacing in the east–west direction (metres).
    dy_m : float
        Grid spacing in the north–south direction (metres).

    Examples
    --------
    >>> import numpy as np
    >>> from data_processing import load_survey_data, prepare_grid
    >>> from utils import compute_grid_spacing_metres
    >>> df = load_survey_data()
    >>> gx, gy = prepare_grid(df["longitude"].values, df["latitude"].values)
    >>> dx, dy = compute_grid_spacing_metres(gx, gy)
    >>> round(dx, 1)
    74.4
    """
    mean_lat = float(np.mean(grid_y))

    meters_per_degree_lat = 111_320.0
    meters_per_degree_lon = 111_320.0 * np.cos(np.radians(mean_lat))

    dx_deg = float(grid_x[1, 0] - grid_x[0, 0])
    dy_deg = float(grid_y[0, 1] - grid_y[0, 0])

    dx_m = dx_deg * meters_per_degree_lon
    dy_m = dy_deg * meters_per_degree_lat

    return dx_m, dy_m


def normalise_array(arr: np.ndarray) -> np.ndarray:
    """
    Min–max normalise an array to [0, 1].

    Parameters
    ----------
    arr : np.ndarray
        Input array (any shape).

    Returns
    -------
    np.ndarray
        Normalised array of the same shape and dtype float64.

    Notes
    -----
    If ``arr.min() == arr.max()`` (constant array), returns an array of
    zeros to avoid division by zero.
    """
    arr = np.asarray(arr, dtype=float)
    arr_min = arr.min()
    arr_max = arr.max()

    if arr_max == arr_min:
        return np.zeros_like(arr)

    return (arr - arr_min) / (arr_max - arr_min)


def percentile_thresholds(
    arr: np.ndarray,
    low_pct: float = 33,
    high_pct: float = 66,
) -> tuple[float, float]:
    """
    Return the low and high percentile values of an array.

    Used throughout the project to split surfaces into three classes.

    Parameters
    ----------
    arr : np.ndarray
        Input array.
    low_pct : float, optional
        Lower percentile (default 33).
    high_pct : float, optional
        Upper percentile (default 66).

    Returns
    -------
    low_threshold : float
    high_threshold : float
    """
    return float(np.percentile(arr, low_pct)), float(np.percentile(arr, high_pct))


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def save_text_output(text: str, path: str) -> None:
    """
    Write *text* to *path* (UTF-8 encoding) and print a confirmation.

    Parameters
    ----------
    text : str
        Content to write.
    path : str
        Destination file path.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved as {path}")


# ---------------------------------------------------------------------------
# Console helpers
# ---------------------------------------------------------------------------

def print_section(title: str, width: int = 60) -> None:
    """
    Print a formatted section header to stdout.

    Parameters
    ----------
    title : str
        Section title text.
    width : int, optional
        Total width of the separator line (default 60).

    Examples
    --------
    >>> print_section("Interpolation Results")
    ============================================================
    Interpolation Results
    ============================================================
    """
    sep = "=" * width
    print(f"\n{sep}")
    print(title)
    print(sep)
