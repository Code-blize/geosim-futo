# References & Technical Stack

## Primary Software & Libraries
*   **Python 3.x:** Core programming language.
*   **NumPy & Pandas:** Vectorized data manipulation and tabular data structures.
*   **SciPy (`scipy.spatial`, `scipy.interpolate`):** Foundation for distance calculations and cross-validation algorithms.
*   **PyProj:** Cartographic transformations and coordinate reference system (CRS) management.
*   **QGIS (Quantum GIS):** Open-source geographic information system utilized for visual validation of spatial outputs and coordinate verification.
*   **Google Colab:** Cloud-based Jupyter notebook environment used for pipeline execution and avoiding local hardware constraints.

## Literature & Methodological References
*   *Inverse Distance Weighting (IDW) Interpolation:* Standard spatial analysis technique for estimating values in un-sampled locations based on the premise of spatial autocorrelation (Tobler's First Law of Geography).
*   *Leave-One-Out Cross-Validation (LOOCV):* Statistical method utilized to assess how the results of a spatial model will generalize to an independent data set, particularly useful for sparse datasets (n=11).
*   *Weighted Overlay Analysis:* A GIS technique utilized for site suitability and hazard mapping by applying a common scale of values to diverse and dissimilar inputs to create an integrated analysis.
