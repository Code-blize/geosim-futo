"""
data_processing.py
------------------
Loads the FUTO VES survey dataset and prepares the interpolation grid.

All raw data originates from the notebook:
  Terrain_Interpolation_Comparison.ipynb (Cells 2–4)
"""

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Hard-coded survey dataset (11 VES stations around FUTO, Owerri, Nigeria)
# ---------------------------------------------------------------------------

_RAW_DATA = {
    "id": [
        "VES_1", "VES_2", "VES_3", "VES_4", "VES_5", "VES_6",
        "VES_7", "VES_8", "VES_9", "VES_10", "VES_11",
    ],
    "longitude": [
        7.016667, 7.000000, 6.983333, 6.983333, 6.966667, 7.000000,
        7.016667, 7.050000, 6.950000, 7.000000, 7.000000,
    ],
    "latitude": [
        5.366667, 5.366667, 5.433333, 5.400000, 5.416667, 5.433333,
        5.400000, 5.450000, 5.433333, 5.400000, 5.383333,
    ],
    "elevation_m": [177, 210, 178, 185, 170, 216, 197, 229, 159, 210, 194],
    "location": [
        "Church, Eziobodo",
        "Girls Sec. School, Eziobodo",
        "Gas Plant, Avu",
        "FUTO Road, Obinze",
        "Church, Obinze",
        "Micoh Guest House Junction, Okowu Village, Nekede",
        "Magistrate Court, Ihiagwa",
        "Industrial Cluster, Nekede",
        "Primary School, Avu",
        "Umuchimma Village Gate, Ihiagwa",
        "Behind Geology Building, FUTO",
    ],
}


def load_survey_data() -> pd.DataFrame:
    """
    Return the FUTO VES elevation survey dataset as a DataFrame.

    Columns
    -------
    id          : station identifier (VES_1 … VES_11)
    longitude   : decimal degrees (WGS-84)
    latitude    : decimal degrees (WGS-84)
    elevation_m : ground elevation in metres
    location    : human-readable place name

    Returns
    -------
    pd.DataFrame
        11 rows × 5 columns.

    Examples
    --------
    >>> from data_processing import load_survey_data
    >>> df = load_survey_data()
    >>> df.shape
    (11, 5)
    """
    return pd.DataFrame(_RAW_DATA)


def prepare_grid(
    x: np.ndarray,
    y: np.ndarray,
    resolution: int = 150,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Build a regular 2-D meshgrid spanning the bounding box of the survey points.

    The grid uses complex-step notation (``150j``) so that ``np.mgrid``
    returns exactly *resolution* nodes in each axis — identical to the
    notebook approach.

    Parameters
    ----------
    x : array-like
        Longitude values of the survey points.
    y : array-like
        Latitude values of the survey points.
    resolution : int, optional
        Number of grid nodes along each axis (default 150).

    Returns
    -------
    grid_x, grid_y : np.ndarray, shape (resolution, resolution)
        2-D arrays of longitude and latitude grid coordinates.

    Examples
    --------
    >>> import numpy as np
    >>> from data_processing import load_survey_data, prepare_grid
    >>> df = load_survey_data()
    >>> gx, gy = prepare_grid(df["longitude"].values, df["latitude"].values)
    >>> gx.shape
    (150, 150)
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    step = complex(0, resolution)   # e.g. 150j
    grid_x, grid_y = np.mgrid[
        x.min() : x.max() : step,
        y.min() : y.max() : step,
    ]
    return grid_x, grid_y
