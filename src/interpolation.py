import numpy as np
import pandas as pd
from scipy.interpolate import griddata


def create_grid(df, resolution=120):
    """
    Create a regular interpolation grid from point data.
    """
    x = df["longitude"].to_numpy()
    y = df["latitude"].to_numpy()
    z = df["elevation_m"].to_numpy()

    grid_x, grid_y = np.mgrid[
        x.min():x.max():resolution*1j,
        y.min():y.max():resolution*1j
    ]

    return x, y, z, grid_x, grid_y


def interpolate_griddata(x, y, z, grid_x, grid_y, method="linear", fill_nans=True):
    """
    Interpolate using scipy.griddata methods: nearest, linear, cubic.
    """
    grid_z = griddata((x, y), z, (grid_x, grid_y), method=method)

    if fill_nans and np.isnan(grid_z).any():
        nearest_fill = griddata((x, y), z, (grid_x, grid_y), method="nearest")
        grid_z = np.where(np.isnan(grid_z), nearest_fill, grid_z)

    return grid_z


def interpolate_idw(x, y, z, grid_x, grid_y, power=2):
    """
    Inverse Distance Weighting (IDW) interpolation.
    """
    sample_points = np.column_stack((x, y))
    grid_points = np.column_stack((grid_x.ravel(), grid_y.ravel()))

    distances = np.sqrt(
        (grid_points[:, None, 0] - sample_points[None, :, 0]) ** 2 +
        (grid_points[:, None, 1] - sample_points[None, :, 1]) ** 2
    )

    distances = np.where(distances == 0, 1e-12, distances)
    weights = 1 / (distances ** power)

    interpolated = (weights @ z) / weights.sum(axis=1)
    return interpolated.reshape(grid_x.shape)


def predict_point_griddata(x_train, y_train, z_train, x0, y0, method="linear"):
    """
    Predict a single point using griddata.
    """
    pred = griddata(
        (x_train, y_train),
        z_train,
        np.array([[x0, y0]]),
        method=method
    )

    if pred is None or np.isnan(pred[0]):
        return np.nan

    return float(pred[0])


def predict_point_idw(x_train, y_train, z_train, x0, y0, power=2):
    """
    Predict a single point using IDW.
    """
    distances = np.sqrt((x_train - x0) ** 2 + (y_train - y0) ** 2)
    distances = np.where(distances == 0, 1e-12, distances)

    weights = 1 / (distances ** power)
    prediction = np.sum(weights * z_train) / np.sum(weights)

    return float(prediction)


def loocv_validation(df, methods=("nearest", "linear", "cubic", "idw"), idw_power=2):
    """
    Leave-One-Out Cross-Validation (LOOCV) for interpolation methods.
    """
    x = df["longitude"].to_numpy()
    y = df["latitude"].to_numpy()
    z = df["elevation_m"].to_numpy()

    results = []

    for method in methods:
        actuals = []
        predictions = []
        errors = []
        skipped = 0

        for i in range(len(df)):
            mask = np.arange(len(df)) != i

            x_train, y_train, z_train = x[mask], y[mask], z[mask]
            x_test, y_test, z_test = x[i], y[i], z[i]

            if method == "idw":
                pred = predict_point_idw(x_train, y_train, z_train, x_test, y_test, power=idw_power)
            else:
                pred = predict_point_griddata(x_train, y_train, z_train, x_test, y_test, method=method)

            if np.isnan(pred):
                skipped += 1
                continue

            actuals.append(z_test)
            predictions.append(pred)
            errors.append(pred - z_test)

        if len(actuals) == 0:
            mae = np.nan
            rmse = np.nan
            mean_error = np.nan
        else:
            actuals = np.array(actuals)
            predictions = np.array(predictions)
            errors = np.array(errors)

            mae = np.mean(np.abs(errors))
            rmse = np.sqrt(np.mean(errors ** 2))
            mean_error = np.mean(errors)

        results.append({
            "method": method,
            "valid_predictions": len(actuals),
            "skipped_predictions": skipped,
            "mae": mae,
            "rmse": rmse,
            "mean_error": mean_error
        })

    return pd.DataFrame(results)


def select_best_method(validation_df):
    """
    Select best method by:
    1. Preferring methods with no skipped predictions
    2. Lowest RMSE
    """
    full_coverage = validation_df[validation_df["skipped_predictions"] == 0]

    if not full_coverage.empty:
        best_row = full_coverage.sort_values("rmse").iloc[0]
    else:
        best_row = validation_df.sort_values("rmse").iloc[0]

    return best_row["method"]
