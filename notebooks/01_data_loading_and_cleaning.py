import pandas as pd

df = pd.read_csv("../data/raw/futo_elevation_points.csv")
print(df.head())
print("\nDataset info:\n")
print(df.info())
print("\nMissing values:\n")
print(df.isnull().sum())
print("\nSummary statistics:\n")
print(df.describe())

import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
scatter = plt.scatter(
    df["longitude"],
    df["latitude"],
    c=df["elevation_m"],
    s=100
)

for _, row in df.iterrows():
    plt.text(row["longitude"], row["latitude"], row["id"], fontsize=8)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Raw Elevation Points Around FUTO")
plt.colorbar(scatter, label="Elevation (m)")
plt.show()
