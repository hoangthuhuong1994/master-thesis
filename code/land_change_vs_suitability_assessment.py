##########################################
# Land cover change within rice suitability assessment
# The code tracking the land cover classes change by tracks transitions at the pixel level
# for each pair of consecutive years (e.g., 1990 vs 1995, 1995 vs 2000, etc.)
# within rice suitable levels
# land cover map classes: 1 urban, 2 rice, 3 others
# rice suitability classes: 1 high suitable, 2 moderate suitable, 3 low suitable, 4 not suitable
##########################################


import os
import rasterio
import numpy as np
import pandas as pd
from collections import defaultdict

# Function to read raster file
def read_raster(file_path):
    print(f"Reading raster file: {file_path}")
    with rasterio.open(file_path) as src:
        nodata_value = src.nodata 
        return src.read(1), nodata_value, src.transform, src.width, src.height

# Function to clip the land cover raster based on the suitability raster
def clip_land_cover_by_suitability(suitability_raster, land_cover_raster, suitability_nodata, land_cover_nodata, suitability_shape):
    land_cover_raster_clipped = land_cover_raster[:suitability_shape[0], :suitability_shape[1]]
    valid_mask = (suitability_raster != suitability_nodata)
    land_cover_raster_clipped = np.where(valid_mask, land_cover_raster_clipped, land_cover_nodata)
    return land_cover_raster_clipped

# Function to compare and track pixel changes from one year to another
def track_pixel_changes(previous_raster, current_raster, suitability_raster, nodata_value):
    changes = defaultdict(lambda: defaultdict(int))  # {suitability_class: {land_cover_class: change} }
    change_to_class = defaultdict(lambda: defaultdict(list))  # {suitability_class: {land_cover_class: [changed_to_classes]}}
    print("Tracking pixel changes from the previous year to the current year...")

    for row in range(suitability_raster.shape[0]):
        for col in range(suitability_raster.shape[1]):
            if previous_raster[row, col] == nodata_value or current_raster[row, col] == nodata_value:
                continue
            # Get the suitability and land cover classes for this pixel
            suitability_class = suitability_raster[row, col]
            previous_class = previous_raster[row, col]
            current_class = current_raster[row, col]

            transition = (previous_class, current_class)
            changes[suitability_class][transition] += 1
            change_to_class[suitability_class][previous_class].append(current_class)

    return changes, change_to_class

# Function to process the data and track changes between consecutive years
def process_changes(suitability_raster, land_cover_rasters, suitability_nodata, land_cover_nodata, suitability_shape):
    year_changes = {}
    change_to_class = {}

    sorted_years = sorted(land_cover_rasters.keys())
    
    # Loop through consecutive years for comparison
    for i in range(len(sorted_years) - 1):
        current_year = sorted_years[i]
        next_year = sorted_years[i + 1]

        # Get the land cover raster for the current and next year
        previous_raster = land_cover_rasters[current_year]
        current_raster = land_cover_rasters[next_year]
        print(f"Processing year pair: {current_year} vs {next_year}")

        # Clip the land cover rasters to match the suitability raster
        previous_raster_clipped = clip_land_cover_by_suitability(suitability_raster, previous_raster, suitability_nodata, land_cover_nodata, suitability_shape)
        current_raster_clipped = clip_land_cover_by_suitability(suitability_raster, current_raster, suitability_nodata, land_cover_nodata, suitability_shape)

        # Compare pixel changes between current and next year
        changes, class_changes = track_pixel_changes(previous_raster_clipped, current_raster_clipped, suitability_raster, land_cover_nodata)
        
        # Store the changes for this year pair
        year_changes[(current_year, next_year)] = changes
        change_to_class[(current_year, next_year)] = class_changes
    return year_changes, change_to_class

# Input files for suitability map and land cover rasters
suitability_file = 'rice_cultivation_suitability.tif'
land_cover_files = {
    1990: '1990_3_class.tif', 
    1995: '1995_3_class.tif',
    2000: '2000_3_class.tif', 
    2005: '2005_3_class.tif', 
    2010: '2010_3_class.tif',
    2015: '2015_3_class.tif', 
    2020: '2020_3_class.tif', 
    2024: '2024_3_class.tif'}

# Read the suitability raster
suitability_raster, suitability_nodata_value, suitability_transform, suitability_width, suitability_height = read_raster(suitability_file)
# Read the land cover rasters for each year
land_cover_rasters = {year: read_raster(file_path)[0] for year, file_path in land_cover_files.items()}

# Process the data and track pixel changes between consecutive years
yearly_changes, class_changes = process_changes(suitability_raster, land_cover_rasters, suitability_nodata_value, None, (suitability_height, suitability_width))

# Convert the results into a pandas DataFrame
def format_changes_to_dataframe(changes, class_changes):
    rows = []

    # Convert changes dictionary into DataFrame rows
    for year_pair, year_changes in changes.items():
        for suitability_class, land_cover_data in year_changes.items():
            for (previous_class, current_class), pixel_change in land_cover_data.items():
                # Record change class transition (including unchanged class transitions like "1 → 1")
                rows.append([year_pair[0], year_pair[1], suitability_class, previous_class, current_class, pixel_change])

    df = pd.DataFrame(rows, columns=['From Year', 'To Year', 'Suitability Class', 'Original Class', 'Change To Class', 'Pixel Change'])
    return df

# Get a formatted DataFrame with pixel changes, total pixel counts, and origin
pixel_changes_df = format_changes_to_dataframe(yearly_changes, class_changes)

# Save the DataFrame to a CSV file
pixel_changes_df.to_csv('land_change_vs_rice_suitability_output.csv', index=False)
print("Data saved to 'land_change_vs_rice_suitability_output.csv'")