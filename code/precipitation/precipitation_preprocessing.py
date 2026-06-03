##########################################
# Precipitation preprocessing
# Subset the study time frame and calculate the average annual precipitation
##########################################

import xarray as xr
import rioxarray

# Load dataset
ds = xr.open_dataset('R.mon.1980-2021_0.10.nc')

# Extract precipitation variable
pr = ds['pr']

# Subset from 1986-01-01 to 2021-12-31
pr_subset = pr.sel(time=slice('1986-01-01', '2021-12-31'))

# Sum monthly precipitation by year
annual_precip = pr_subset.groupby('time.year').sum(dim='time')

# Calculate mean annual precipitation over years
mean_annual_precip = annual_precip.mean(dim='year')

# Define nodata value
nodata_val = 0

# Fill NaNs with nodata value
mean_annual_precip_filled = mean_annual_precip.fillna(nodata_val)

# Assign CRS if missing (assumed WGS84 lat/lon)
if not mean_annual_precip_filled.rio.crs:
    mean_annual_precip_filled = mean_annual_precip_filled.rio.write_crs("EPSG:4326")

# Set the nodata value explicitly
mean_annual_precip_filled.rio.write_nodata(nodata_val, inplace=True)

# Export to GeoTIFF
output_path = 'precipitation.tif'
mean_annual_precip_filled.rio.to_raster(output_path)
print(f"GeoTIFF exported with nodata={nodata_val}: {output_path}")