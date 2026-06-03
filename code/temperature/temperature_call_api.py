##########################################
# Minimum temperature for January and February from 1986 to 2024
# Data cource: https://cds.climate.copernicus.eu/how-to-api
##########################################

import cdsapi
import os

def download_data(start_year, end_year):
    folder = "temp_daily_min"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for year in range(start_year, end_year + 1):
        for month in [1, 2]:  # January (1) and February (2)
            month_str = str(month).zfill(2)
            request = {
                "variable": ["2m_temperature"],
                "year": str(year),
                "month": month_str,
                "day": [str(day).zfill(2) for day in range(1, 32)],  # Days 01 to 31
                "daily_statistic": "daily_minimum",
                "time_zone": "utc+07:00",
                "frequency": "6_hourly",
                "area": [22, 104.5, 19.5, 108.5]
            }

            output_filename = os.path.join(folder, f"min_temp_{month_str}_{year}.nc")
            
            client = cdsapi.Client()
            print(f"Downloading data for {month_str}-{year}...")
            client.retrieve("derived-era5-land-daily-statistics", request).download(output_filename)
            print(f"Download completed for {month_str}-{year}.")

# Download data from 1986 to 2024
download_data(1986, 2024)

