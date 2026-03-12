## imports and path setup

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(".."))

from src.interpolation import (
    create_grid,
    interpolate_griddata,
    interpolate_idw,
    loocv_validation,
    select_best_method
)


## load the dataset

df = pd.read_csv("../data/raw/futo_elevation_points.csv")
df

##create interpolation grid

x, y, z, grid_x, grid_y = create_grid(df, resolution=150)

print("Number of sample points:", len(df))
print("Grid shape:", grid_x.shape)

## generate terrain surfaces using different methods

surfaces = {
    "nearest": interpolate_griddata(x, y, z, grid_x, grid_y, method="nearest"),
    "linear": interpolate_griddata(x, y, z, grid_x, grid_y, method="linear"),
    "cubic": interpolate_griddata(x, y, z, grid_x, grid_y, method="cubic"),
    "idw": interpolate_idw(x, y, z, grid_x, grid_y, power=2)
}

## compare interpolation methods in 2D

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.ravel()

for ax, (method, surface) in zip(axes, surfaces.items()):
    contour = ax.contourf(grid_x, grid_y, surface, levels=20, cmap="terrain")
    ax.scatter(x, y, c=z, cmap="terrain", edgecolor="black", s=60)
    ax.set_title(f"{method.upper()} Interpolation")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    fig.colorbar(contour, ax=ax, shrink=0.8, label="Elevation (m)")

plt.tight_layout()
plt.show()

## compare interpolation methods in 3D

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig = plt.figure(figsize=(16, 12))

for i, (method, surface) in enumerate(surfaces.items(), start=1):
    ax = fig.add_subplot(2, 2, i, projection="3d")
    ax.plot_surface(grid_x, grid_y, surface, cmap="terrain", edgecolor="none", alpha=0.9)
    ax.scatter(x, y, z, s=40, c="red")
    ax.set_title(f"{method.upper()} Surface")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Elevation (m)")

plt.tight_layout()
plt.show()

## run validation

validation_df = loocv_validation(df, methods=("nearest", "linear", "cubic", "idw"), idw_power=2)
validation_df.sort_values("rmse")


## choose best method

best_method = select_best_method(validation_df)
print("Best interpolation method:", best_method)

## visualize the selected best surface clearly

best_surface = surfaces[best_method]

plt.figure(figsize=(10, 7))
contour = plt.contourf(grid_x, grid_y, best_surface, levels=25, cmap="terrain")
plt.scatter(x, y, c=z, cmap="terrain", edgecolor="black", s=80)

for _, row in df.iterrows():
    plt.text(row["longitude"], row["latitude"], row["id"], fontsize=8)

plt.title(f"Selected Terrain Surface Using {best_method.upper()}")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.colorbar(contour, label="Elevation (m)")
plt.show()

## create contour lines

plt.figure(figsize=(10, 7))
filled = plt.contourf(grid_x, grid_y, best_surface, levels=20, cmap="terrain")
lines = plt.contour(grid_x, grid_y, best_surface, levels=10, colors="black", linewidths=0.6)

plt.clabel(lines, inline=True, fontsize=8)
plt.scatter(x, y, c="red", s=50)
plt.title(f"Contour Map from {best_method.upper()} Surface")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.colorbar(filled, label="Elevation (m)")
plt.show()

## save outputs into your repo structure

os.makedirs("../data/processed", exist_ok=True)
os.makedirs("../outputs/figures", exist_ok=True)

terrain_grid_df = pd.DataFrame({
    "longitude": grid_x.ravel(),
    "latitude": grid_y.ravel(),
    "elevation_m": best_surface.ravel()
})

terrain_grid_df.to_csv("../data/processed/futo_terrain_grid.csv", index=False)
validation_df.to_csv("../data/processed/interpolation_validation_results.csv", index=False)

print("Saved:")
print("- ../data/processed/futo_terrain_grid.csv")
print("- ../data/processed/interpolation_validation_results.csv")
