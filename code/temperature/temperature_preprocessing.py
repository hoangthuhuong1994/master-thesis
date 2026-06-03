##########################################
# Minimum temperature pre-processing
# temperature is converted from Kelvin to Celsius and Calculate the mean temperature 
##########################################


import os
import glob
import rioxarray
import xarray as xr

# Define the folder paths
input_folder = 'temp_daily_min'
output_folder = './mean_min_temp'

# Step 1: List all NetCDF files in the input folder matching the pattern
nc_files = glob.glob(os.path.join(input_folder, 'min_temp_*_*.nc'))

# Step 2: Group files by month (extract month from filename)
file_groups = {}
for nc_file in nc_files:
    filename = os.path.basename(nc_file)
    month = filename.split('_')[2]  # Extract month from filename
    
    if month not in file_groups:
        file_groups[month] = []
    file_groups[month].append(nc_file)

# Step 3: Process each group of files (grouped by month)
monthly_mean_temperatures = []  # List to store monthly mean temperatures for overall mean calculation

for month in sorted(file_groups.keys()):
    monthly_mean_temperatures_in_group = []  # List to store the mean temperatures for all files in this month

    for nc_file in file_groups[month]:
        dataset = xr.open_dataset(nc_file)
        
        # Step 4: Check and assign CRS if not present
        if dataset.rio.crs is None:
            dataset = dataset.rio.write_crs("epsg:4326", inplace=True)

        # Step 5: Convert temperature from Kelvin to Celsius
        temperature_celsius = dataset["t2m"] - 273.15

        # Step 6: Calculate the mean temperature over the 'valid_time' dimension
        temperature_mean = temperature_celsius.mean(dim='valid_time')

        monthly_mean_temperatures_in_group.append(temperature_mean)

    # Step 7: Calculate the overall monthly mean temperature
    num_files = len(file_groups[month])
    monthly_mean_temperature = sum(monthly_mean_temperatures_in_group) / num_files
    monthly_mean_temperatures.append(monthly_mean_temperature)

    # Step 8: Save the GeoTIFF for the monthly mean temperature
    output_tiff_filename = os.path.join(output_folder, f'mean_min_temp_{month.zfill(2)}.tif')
    monthly_mean_temperature.rio.to_raster(output_tiff_filename)

# Step 9: Calculate the overall mean temperature across all months (12 months)
overall_mean_temperature = sum(monthly_mean_temperatures) / len(monthly_mean_temperatures)

# Step 10: Save the overall mean temperature to a GeoTIFF
output_overall_tiff_filename = os.path.join(output_folder, 'average_min_temperature.tif')
overall_mean_raster = monthly_mean_temperatures[0].copy()  # Use the first month's raster as template
overall_mean_raster[:] = overall_mean_temperature  # Set all values to the overall mean temperature
overall_mean_raster.rio.to_raster(output_overall_tiff_filename)
