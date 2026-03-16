"""
visualization.py
----------------
All plotting functions for the GeoSim FUTO project — both static
(Matplotlib) and interactive (Plotly).

Notebook source: Cells 8–9, 15, 18, 21, 27, 29, 33, 37, 42, 44, 46, 50
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)


# ---------------------------------------------------------------------------
# Static (Matplotlib) — interpolation surfaces
# ---------------------------------------------------------------------------

def plot_interpolation_comparison(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    surfaces: dict[str, np.ndarray],
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
) -> None:
    """
    2×2 grid of filled-contour plots, one per interpolation method.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    surfaces : dict[str, np.ndarray]
        Mapping of method name → elevation surface
        (e.g. ``{"Nearest": ..., "Linear": ..., "Cubic": ..., "IDW": ...}``).
    x, y, z : np.ndarray
        Survey point coordinates and elevations (plotted as scatter).
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.ravel()

    for ax, (name, surface) in zip(axes, surfaces.items()):
        contour = ax.contourf(grid_x, grid_y, surface, levels=20, cmap="terrain")
        ax.scatter(x, y, c=z, cmap="terrain", edgecolor="black", s=60)
        ax.set_title(f"{name} Interpolation")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        fig.colorbar(contour, ax=ax, shrink=0.8, label="Elevation (m)")

    plt.tight_layout()
    plt.show()


def plot_3d_surfaces(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    surfaces: dict[str, np.ndarray],
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
) -> None:
    """
    2×2 grid of 3-D surface plots, one per interpolation method.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    surfaces : dict[str, np.ndarray]
        Elevation surfaces keyed by method name.
    x, y, z : np.ndarray
        Survey point coordinates and elevations (plotted as red dots).
    """
    plt.style.use("dark_background")
    fig = plt.figure(figsize=(16, 12))

    for i, (name, surface) in enumerate(surfaces.items(), start=1):
        ax = fig.add_subplot(2, 2, i, projection="3d")
        ax.plot_surface(grid_x, grid_y, surface, cmap="terrain", edgecolor="none", alpha=0.9)
        ax.scatter(x, y, z, c="red", s=40)
        ax.set_title(f"{name} Surface")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_zlabel("Elevation (m)")

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Static — terrain analysis
# ---------------------------------------------------------------------------

def plot_idw_contour(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    idw_surface: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
) -> None:
    """
    Filled-contour map of the IDW terrain surface with labelled contour lines.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    idw_surface : np.ndarray
        IDW elevation surface.
    x, y : np.ndarray
        Survey point coordinates (plotted as red dots).
    """
    plt.figure(figsize=(10, 7))

    filled = plt.contourf(grid_x, grid_y, idw_surface, levels=20, cmap="terrain")
    lines  = plt.contour(grid_x, grid_y, idw_surface, levels=10, colors="black", linewidths=0.7)

    plt.clabel(lines, inline=True, fontsize=8)
    plt.scatter(x, y, c="red", s=50, label="Measured Points")

    plt.title("Contour Map from IDW Terrain Surface")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.colorbar(filled, label="Elevation (m)")
    plt.legend()
    plt.show()


def plot_slope_map(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    slope_degrees: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
) -> None:
    """
    Filled-contour map of slope in degrees derived from the IDW surface.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    slope_degrees : np.ndarray
        Slope surface (degrees).
    x, y : np.ndarray
        Survey point coordinates (plotted as red dots).
    """
    plt.figure(figsize=(10, 7))

    slope_plot = plt.contourf(grid_x, grid_y, slope_degrees, levels=20, cmap="viridis")
    plt.scatter(x, y, c="red", s=40, label="Measured Points")

    plt.title("Slope Map Derived from IDW Surface")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.colorbar(slope_plot, label="Slope (degrees)")
    plt.legend()
    plt.show()


def plot_terrain_classification(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    terrain_class: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
) -> None:
    """
    Classified terrain map (Lowland / Midland / Highland).

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    terrain_class : np.ndarray
        Integer class array (1, 2, 3).
    x, y : np.ndarray
        Survey point coordinates (plotted as black dots).
    """
    plt.figure(figsize=(10, 7))

    class_plot = plt.contourf(
        grid_x, grid_y, terrain_class,
        levels=[0.5, 1.5, 2.5, 3.5],
        cmap="terrain",
    )
    plt.scatter(x, y, c="black", s=40)

    plt.title("Terrain Classification from IDW Elevation Surface")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    cbar = plt.colorbar(class_plot, ticks=[1, 2, 3])
    cbar.ax.set_yticklabels(["Lowland", "Midland", "Highland"])

    plt.show()


# ---------------------------------------------------------------------------
# Static — flood susceptibility
# ---------------------------------------------------------------------------

def plot_flood_susceptibility(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    flood_susceptibility: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
) -> None:
    """
    Continuous flood susceptibility surface map.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    flood_susceptibility : np.ndarray
        Continuous susceptibility index.
    x, y : np.ndarray
        Survey point coordinates (plotted as black dots).
    """
    plt.figure(figsize=(10, 7))

    risk_plot = plt.contourf(grid_x, grid_y, flood_susceptibility, levels=20, cmap="RdYlBu_r")
    plt.scatter(x, y, c="black", s=40, label="Measured Points")

    plt.title("Flood Susceptibility Map")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.colorbar(risk_plot, label="Flood Susceptibility Index")
    plt.legend()
    plt.show()


def plot_classified_flood_risk(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    risk_class: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
) -> None:
    """
    Discrete flood risk zone map (Low / Moderate / High).

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    risk_class : np.ndarray
        Integer risk class array (1, 2, 3).
    x, y : np.ndarray
        Survey point coordinates (plotted as black dots).
    """
    plt.figure(figsize=(10, 7))

    classified_plot = plt.contourf(
        grid_x, grid_y, risk_class,
        levels=[0.5, 1.5, 2.5, 3.5],
        cmap="YlOrRd",
    )
    plt.scatter(x, y, c="black", s=40)

    plt.title("Classified Flood Susceptibility Zones")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    cbar = plt.colorbar(classified_plot, ticks=[1, 2, 3])
    cbar.ax.set_yticklabels(["Low", "Moderate", "High"])

    plt.show()


# ---------------------------------------------------------------------------
# Static — inundation scenarios
# ---------------------------------------------------------------------------

def plot_inundation_scenarios(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    masks: dict[str, np.ndarray],
    summary_df: pd.DataFrame,
    x: np.ndarray,
    y: np.ndarray,
) -> None:
    """
    Side-by-side inundation masks for Mild, Moderate, and Severe scenarios.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    masks : dict[str, np.ndarray of bool]
        Boolean inundation masks keyed by scenario name.
    summary_df : pd.DataFrame
        Summary table with ``scenario`` and ``water_level_m`` columns.
    x, y : np.ndarray
        Survey point coordinates (plotted as red dots).
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for ax, (scenario_name, mask) in zip(axes, masks.items()):
        level = summary_df.loc[
            summary_df["scenario"] == scenario_name, "water_level_m"
        ].values[0]

        ax.contourf(grid_x, grid_y, mask, levels=[-0.1, 0.1, 1], cmap="Blues")
        ax.scatter(x, y, c="red", s=35)
        ax.set_title(f"{scenario_name} Inundation\nWater Level = {level:.2f} m")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

    plt.tight_layout()
    plt.show()


def plot_inundation_bar(summary_df: pd.DataFrame) -> None:
    """
    Bar chart of inundated terrain percentage per scenario.

    Parameters
    ----------
    summary_df : pd.DataFrame
        From :func:`simulation.build_inundation_scenarios`.
    """
    plt.figure(figsize=(8, 5))
    plt.bar(summary_df["scenario"], summary_df["inundated_percent"])
    plt.title("Percentage of Inundated Terrain by Scenario")
    plt.xlabel("Scenario")
    plt.ylabel("Inundated Area (%)")
    plt.show()


# ---------------------------------------------------------------------------
# Static — semantic scene zones
# ---------------------------------------------------------------------------

def plot_scene_zones(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    scene_zone: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
) -> None:
    """
    Semantic scene zone map with a four-colour legend.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    scene_zone : np.ndarray
        Integer zone array (1–4).
    x, y : np.ndarray
        Survey point coordinates (plotted as black dots).
    """
    scene_cmap = ListedColormap(["royalblue", "khaki", "forestgreen", "lightgray"])
    scene_norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5], scene_cmap.N)

    plt.figure(figsize=(10, 7))
    scene_plot = plt.contourf(
        grid_x, grid_y, scene_zone,
        levels=[0.5, 1.5, 2.5, 3.5, 4.5],
        cmap=scene_cmap,
        norm=scene_norm,
    )

    plt.scatter(x, y, c="black", s=40)
    plt.title("Semantic Scene Zones for Generative Visualization")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    cbar = plt.colorbar(scene_plot, ticks=[1, 2, 3, 4])
    cbar.ax.set_yticklabels(["Wet Lowland", "Transitional Midland", "Stable Upland", "Mixed Terrain"])

    plt.show()


# ---------------------------------------------------------------------------
# Interactive (Plotly)
# ---------------------------------------------------------------------------

def _require_plotly():
    """Lazy import guard — raises a clear error if plotly is not installed."""
    try:
        import plotly.graph_objects as go
        return go
    except ImportError as exc:
        raise ImportError(
            "plotly is required for interactive visualizations. "
            "Install it with:  pip install plotly"
        ) from exc


def plot_interactive_terrain(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    idw_surface: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    station_ids: list[str],
    save_html: str | None = "futo_interactive_terrain.html",
) -> object:
    """
    Interactive 3-D terrain model coloured by elevation.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    idw_surface : np.ndarray
        IDW elevation surface.
    x, y, z : np.ndarray
        Survey point coordinates and elevations.
    station_ids : list[str]
        Labels for the scatter markers (e.g. VES_1 … VES_11).
    save_html : str or None, optional
        If given, the figure is saved as an HTML file.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _require_plotly()

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=grid_x, y=grid_y, z=idw_surface,
        colorscale="earth",
        colorbar=dict(title="Elevation (m)"),
        opacity=0.95,
    ))

    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode="markers+text",
        marker=dict(size=5, color="red"),
        text=station_ids,
        textposition="top center",
        name="Measured Points",
    ))

    fig.update_layout(
        title="Interactive 3D Terrain Model of the FUTO Study Area",
        scene=dict(
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            zaxis_title="Elevation (m)",
        ),
        width=950,
        height=700,
    )

    fig.show()

    if save_html:
        fig.write_html(save_html)
        print(f"Saved as {save_html}")

    return fig


def plot_interactive_flood_susceptibility(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    idw_surface: np.ndarray,
    flood_susceptibility: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    station_ids: list[str],
    save_html: str | None = "futo_3d_flood_susceptibility.html",
) -> object:
    """
    Interactive 3-D terrain coloured by normalised flood susceptibility.

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    idw_surface : np.ndarray
        IDW elevation surface (used for 3-D shape).
    flood_susceptibility : np.ndarray
        Raw (un-normalised) susceptibility values (normalised internally).
    x, y, z : np.ndarray
        Survey point coordinates and elevations.
    station_ids : list[str]
        Marker labels.
    save_html : str or None, optional
        Output HTML file path.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _require_plotly()

    sus_min = float(np.min(flood_susceptibility))
    sus_max = float(np.max(flood_susceptibility))
    sus_norm = (flood_susceptibility - sus_min) / (sus_max - sus_min)

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=grid_x, y=grid_y, z=idw_surface,
        surfacecolor=sus_norm,
        colorscale="RdYlBu_r",
        colorbar=dict(title="Normalized Flood Susceptibility"),
        opacity=0.97,
    ))

    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode="markers+text",
        marker=dict(size=5, color="black"),
        text=station_ids,
        textposition="top center",
        name="Measured Points",
    ))

    fig.update_layout(
        title="3D Terrain with Flood Susceptibility Overlay",
        scene=dict(
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            zaxis_title="Elevation (m)",
        ),
        width=950,
        height=700,
    )

    fig.show()

    if save_html:
        fig.write_html(save_html)
        print(f"Saved as {save_html}")

    return fig


def plot_interactive_inundation_scenario(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    idw_surface: np.ndarray,
    inundation_mask: np.ndarray,
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    station_ids: list[str],
    scenario_name: str = "Moderate",
    save_html: str | None = "futo_moderate_inundation_scenario.html",
) -> object:
    """
    Interactive 3-D terrain coloured tan (dry) / blue (inundated).

    Parameters
    ----------
    grid_x, grid_y : np.ndarray
        Meshgrid coordinates.
    idw_surface : np.ndarray
        IDW elevation surface.
    inundation_mask : np.ndarray of bool
        Boolean mask — ``True`` where inundated.
    x, y, z : np.ndarray
        Survey point coordinates and elevations.
    station_ids : list[str]
        Marker labels.
    scenario_name : str, optional
        Used only in the figure title (default ``"Moderate"``).
    save_html : str or None, optional
        Output HTML file path.

    Returns
    -------
    plotly.graph_objects.Figure
    """
    go = _require_plotly()

    overlay = np.where(inundation_mask, 1, 0)

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=grid_x, y=grid_y, z=idw_surface,
        surfacecolor=overlay,
        colorscale=[
            [0.0,   "tan"],
            [0.499, "tan"],
            [0.5,   "blue"],
            [1.0,   "blue"],
        ],
        showscale=False,
        opacity=0.97,
    ))

    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode="markers+text",
        marker=dict(size=5, color="red"),
        text=station_ids,
        textposition="top center",
        name="Measured Points",
    ))

    fig.update_layout(
        title=f"3D {scenario_name} Inundation Scenario",
        scene=dict(
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            zaxis_title="Elevation (m)",
        ),
        width=950,
        height=700,
    )

    fig.show()

    if save_html:
        fig.write_html(save_html)
        print(f"Saved as {save_html}")

    return fig
