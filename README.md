# master-thesis
Master Thesis Topic: Assessing Land Cover Changes and Rice Cultivation Suitability in Vietnam’s Red River Delta

**Author:** Thi Thu Huong Hoang | **Supervisors:** JProf. Dr. David Frantz, Dr. Achim Röder

## Overview
The study monitor the spatial and temporal dynamics of urban expansion and its impacts on rice-growing areas in the Red River Delta in Vietnam from 1986 to 2024 and assesses the suitability of the region for rice cultivation.

## Main objectives:
  •	Map and analyze urban and rice land cover changes over 38 years using remote sensing imagery.
  • Generate a rice cultivation suitability map using multi-criteria decision analysis (MCDA).
  •	Assessing land cover changes on rice suitability across the broader of the study area.

## Key Findings

• Urban areas expanded steadily across all 11 provinces, with Hanoi showing the largest growth (~76,000 ha gained).
• Rice loss accelerated in recent years, exceeding 90,000 ha in 2024, driven by urbanization, crop conversion and field abandonment.
• 65.4% of the Red River Delta is classified as high or moderate suitable for rice cultivation.


## Methodology
###  Phase 1 — Land Cover Change Analysis

Data: Landsat 4/5/7/8/9 imagery (3,561 scenes, 30 m resolution)
Preprocessing: FORCE framework — atmospheric correction, cloud masking, data cubing
Features: Spectral Temporal Metrics (STMs) over 5-year intervals; spectral bands + indices (EVI, NDBI, SAVI, NDWI)
Classification: Random Forest (RF) with 800 training points across 8 land cover classes
Change detection: Post-Classification Comparison (PCC); accuracy assessed following Olofsson et al. (2014)

### Phase 2 — Rice Cultivation Suitability

Criteria: Soil texture, soil pH, minimum temperature, elevation, slope, distance to rivers/streams, precipitation
Weighting: Analytic Hierarchy Process (AHP)
Output: Normalized Suitability Index mapped to 4 levels (high / moderate / low / not suitable)

# Phase 3 — Land cover change within rice suitability assessment

Approach: Pixel-level cross-overlay of urban and rice change maps with the rice suitability zones across all time intervals (1990–2024)
Land cover classes: Urban, rice, and others (aquaculture, water bodies, forests, bare soil, other crops)
Suitability zones: High suitable, moderate suitable, low suitable, not suitable
Output:
  • Urban expansion occurred predominantly in high and moderate suitable zones. In Hanoi, ~22,500 ha (high) and ~52,100 ha (moderate) were converted to urban
  • Land transitions in low suitable and not suitable zones were minimal throughout the study period

## Tools & Data Sources

| Tool / Dataset | Purpose |
|---|---|
| [FORCE](https://force-eo.readthedocs.io/) | Landsat preprocessing & STM generation & Classification |
| QGIS 3.40.5 | Raster analysis, suitability mapping |
| Python, R | accuracy assessment, pixel-level raster overlay, transition tracking)|
| Landsat Archive (USGS) | Earth observation imagery |
| Copernicus ERA5-Land | Temperature & precipitation |
| Copernicus GLO-30 DEM | Elevation & slope |
| SoilGrids (ISRIC) | Soil texture & pH |
| OpenStreetMap (Overpass API) | Rivers & streams |

### Repository Structure

```
├── code/
│   ├── temperature/
│   │  ├── temperature_call_api.py   # ERA5 temperature download & preprocessing
│   │  ├── temperature_preprocessing.py
│   ├── precipitation/
│   │  ├── precipitation_interpolation_IDW.py  
│   │  ├── precipitation_preprocessing.py
│   ├── download_ph_sand_silt_clay_rivers.txt    # Sand, silt, clay, pH download via GEE
│   ├── rivers_overpass.txt         # OSM rivers/streams query
│   ├── urban_rice_assessment.py    # Urban–rice cross-analysis
│   └── land_change_vs_suitability_assessment.py  # Land cover × suitability level analysis
├── results/                        # Output maps and accuracy tables
└── README.md
```
