##########################################
# Precipitation interpolation using IDW (Inverse Distance Weighting)
##########################################

import numpy as np
from osgeo import gdal
from scipy.spatial.distance import cdist

def idw_interpolation(valid_coords, valid_data, grid_coords, power=2, epsilon=1e-10):
    """
    Perform IDW interpolation.
    valid_coords: Coordinates of valid data points.
    valid_data: Values at valid data points.
    grid_coords: Coordinates of the grid points to interpolate.
    power: Power parameter for IDW. Default is 2.
    epsilon: Small value added to distances to avoid divide by zero errors. Default is 1e-10.
    """
    # Compute distances between grid points and valid data points
    distances = cdist(grid_coords, valid_coords)
    
    # Avoid divide by zero by adding epsilon to distances
    distances = np.maximum(distances, epsilon)
    
    # Apply IDW formula (1/d^power)
    weights = 1 / (distances ** power)
    
    # Normalize weights (so they sum to 1)
    weights /= weights.sum(axis=1)[:, np.newaxis]
    
    # Interpolate the values
    interpolated_values = np.dot(weights, valid_data)
    return interpolated_values

def interpolate_nodata(input_raster, output_raster, power=2):
    # Open the raster
    dataset = gdal.Open(input_raster)
    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray()
    
    # Define the target value to interpolate (in this case, 0)
    nodata_value = 0

    # Get raster dimensions
    rows, cols = data.shape

    # Create grid coordinates (pixel positions)
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    grid_coords = np.column_stack((x.ravel(), y.ravel()))

    # Mask for target pixels (value == 0)
    nodata_mask = data == nodata_value  # Mask where the data is '0'

    # Get valid data (non-target pixels)
    valid_data = data[~nodata_mask]
    valid_coords = np.column_stack((x[~nodata_mask], y[~nodata_mask]))

    # Interpolate the target pixels using IDW
    interpolated_values = idw_interpolation(valid_coords, valid_data, grid_coords, power)

    # Reshape the interpolated values back into the raster shape
    interpolated_values = interpolated_values.reshape((rows, cols))

    # Replace target pixels with interpolated values
    data[nodata_mask] = interpolated_values[nodata_mask]

    # Save the interpolated raster
    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(output_raster, cols, rows, 1, gdal.GDT_Float32)
    out_raster.SetGeoTransform(dataset.GetGeoTransform())
    out_raster.SetProjection(dataset.GetProjection())

    # Write the modified data
    out_band = out_raster.GetRasterBand(1)
    out_band.SetNoDataValue(nodata_value)
    out_band.WriteArray(data)

    # Clean up
    out_raster = None
    dataset = None
    print(f"Output raster saved as {output_raster}")

# Example usage:
interpolate_nodata('precipitation.tif', 'precipitation_idw.tif', power=2)
