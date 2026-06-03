##########################################
# Analyzing Urban and rice change assessment
#This script performs an analysis by combining two datasets: urban and rice change maps 
# To identify the relationship between rice loss and urban gain across years.
##########################################

import os
import rasterio
import numpy as np
import pandas as pd

# output directory 
csv_output_directory = 'urban_rice_assessment_output/'

if not os.path.exists(csv_output_directory):
    os.makedirs(csv_output_directory)

# Define the class values for rice loss and urban gain for each year
# These dictionaries map years to the corresponding class values in the classification rasters

# class 16: rice loss in 1995, 15 rice loss in 2000, 14 rice loss in 2005, 13 rice loss in 2010, 12 rice loss in 2015
# 11 rice loss in 2020, 10 rice loss in 2024
rice_loss_classes = {1995: 16, 2000: 15, 2005: 14, 2010: 13, 2015: 12, 2020: 11, 2024: 10}

# class 9: urban gain in 1995, 8: urban gain in 2000, 7: urban gain in 2005, 6: urban gain in 2010, 5: urban gain in 2015, 
# 4: urban gain in 2020, 3: urban gain in 2024
urban_gain_classes = {1995: 9, 2000: 8, 2005: 7, 2010: 6, 2015: 5, 2020: 4, 2024: 3}

# Open the rice and urban classification rasters
with rasterio.open('rice_validation.tif') as src_rice:
    rice_classification = src_rice.read(1)  # Read the first band (the rice loss data)
    meta_rice = src_rice.meta  # Store the metadata (coordinate reference system, transform, etc.)

with rasterio.open('urban_validation.tif') as src_urban:
    urban_classification = src_urban.read(1)  # Read the first band (the urban gain data)

# Loop through each combination of rice loss and urban gain years
# The combination is based on the keys in the rice_loss_classes and urban_gain_classes dictionaries
for rice_year, rice_class in rice_loss_classes.items():
    for urban_year, urban_class in urban_gain_classes.items():
        rice_loss_binary = np.where(rice_classification == rice_class, 1, 0)
        urban_gain_binary = np.where(urban_classification == urban_class, 1, 0)

        # Perform Cross-Classification (1 = rice loss, 2 = urban gain)
        # The cross-classification assigns:
        # - Class 0: pixel contain neither rice loss nor urban gain (where rice_loss_binary == 0 and urban_gain_binary == 0)        
        # - Class 1: rice loss only (where rice_loss_binary == 1 and urban_gain_binary == 0)
        # - Class 2: urban gain only (where rice_loss_binary == 0 and urban_gain_binary == 1)
        # - Class 3: both rice loss and urban gain (where both binary masks have value 1)
        cross_classified = rice_loss_binary + urban_gain_binary * 2

        # Create a Pandas DataFrame for easier analysis of the cross-classified raster data
        # Flatten the 2D array into 1D to create a table of pixel classes
        tabulation = pd.DataFrame(cross_classified.flatten(), columns=['Class'])

        # Count the number of occurrences of each class (how many pixels fall into each class)
        class_counts = tabulation['Class'].value_counts()

        # Save the class counts as a CSV file for future reanalysis
        class_counts.to_csv(f'{csv_output_directory}urban_rice_results_{rice_year}_{urban_year}.csv')
