#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Nov  11, 2024

Lesson 6. Calculate Seasonal Summary Values from Climate Data Variables 
Stored in NetCDF 4 Format: Work With MACA v2 Climate Data in Python

from: https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/summarize-climate-data-by-season/

@author: bblrd
"""

# Import packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import earthpy as et
import xarray as xr
import regionmask

# Plotting options
sns.set(font_scale=1.3)
sns.set_style("white")

# Optional - set your working directory if you wish to use the data
# accessed lower down in this notebook (the USA state boundary data)
os.chdir(os.path.join(et.io.HOME,
                      'earth-analytics',
                      'data'))


#%% #################

# To begin, you can download and open up a MACA v2 netcdf file. The file below is a projected 
# maximum temperature dataset downscaled using the BNU-ESM model for 2006-2099.

# Get netcdf file
data_path_monthly = 'http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_macav2metdata_tasmax_BNU-ESM_r1i1p1_rcp45_2006_2099_CONUS_monthly.nc'

# Open up the data
with xr.open_dataset(data_path_monthly) as file_nc:
    monthly_forecast_temp_xr = file_nc

# xarray object
monthly_forecast_temp_xr

#%% #################

# In the example below you subset data for the state of California similar to what you 
# did in the previous lesson. You can select any state that you wish for this analysis!

# Download natural earth data to generate AOI
url =  (
    "https://naturalearth.s3.amazonaws.com/"
    "50m_cultural/ne_50m_admin_1_states_provinces_lakes.zip"
)
states_gdf = gpd.read_file(url)
cali_aoi = states_gdf[states_gdf.name == "California"]

#%% #################

# Would this be better if it only returned 4 values?? probably so
# Helper Function to extract AOI
def get_aoi(shp, world=True):
    """Takes a geopandas object and converts it to a lat/ lon
    extent """

    lon_lat = {}
    # Get lat min, max
    aoi_lat = [float(shp.total_bounds[1]), float(shp.total_bounds[3])]
    aoi_lon = [float(shp.total_bounds[0]), float(shp.total_bounds[2])]

    # Handle the 0-360 lon values
    if world:
        aoi_lon[0] = aoi_lon[0] + 360
        aoi_lon[1] = aoi_lon[1] + 360
    lon_lat["lon"] = aoi_lon
    lon_lat["lat"] = aoi_lat
    return lon_lat

#%% #################

# Get lat min, max from Cali aoi extent
cali_bounds = get_aoi(cali_aoi)

# Slice by time & aoi location
start_date = "2059-12-15"
end_date = "2099-12-15"

cali_temp = monthly_forecast_temp_xr["air_temperature"].sel(
    time=slice(start_date, end_date),
    lon=slice(cali_bounds["lon"][0], cali_bounds["lon"][1]),
    lat=slice(cali_bounds["lat"][0], cali_bounds["lat"][1]))
cali_temp

#%% #################

print("Time Period start: ", cali_temp.time.min().values)
print("Time Period end: ", cali_temp.time.max().values)

#%% #################

# Create the region mask object - this is used to identify each region
# cali_region = regionmask.from_geopandas(cali_aoi,
#                                         names="name",
#                                         name="name",
#                                         abbrevs="iso_3166_2")
cali_mask = regionmask.mask_3D_geopandas(cali_aoi,
                                         monthly_forecast_temp_xr.lon,
                                         monthly_forecast_temp_xr.lat)
# Mask the netcdf data
cali_temp_masked = cali_temp.where(cali_mask)
cali_temp_masked.dims

#%% #################

cali_temp.values.shape

#%% #################


cali_season_summary = cali_temp_masked.groupby(
    'time.season').mean('time', skipna=True)

# This will create 4 arrays - one for each season showing mean temperature values
cali_season_summary.shape

#%% #################

# Create a plot showing mean temperature aross seasons
cali_season_summary.plot(col='season', col_wrap=2, figsize=(10, 10))
plt.suptitle("Mean Temperature Across All Selected Years By Season \n California, USA",
             y=1.05)

plt.show()


#%% #################

# Calculate UnWeighted Seasonal Averages For By Season Across Each Year
# Above you created one single value per season which summarized seasonal data across all years. 
# However you may want to look at seasonal variation year to year in the projected data. You can 
# calculate seasonal statistcs by:
# (1) resampling the data and then (2) grouping the data and summarizing it

# Resample the data by season across all years
cali_season_mean_all_years = cali_temp_masked.resample(
    time='QS-DEC', keep_attrs=True).mean()
cali_season_mean_all_years.shape

#%% #################

# Summarize each array into one single (mean) value
cali_seasonal_mean = cali_season_mean_all_years.groupby('time').mean([
    "lat", "lon"])
cali_seasonal_mean.shape

#%% #################

# This data now has one value per season rather than an array
cali_seasonal_mean.shape


#%% #################

# Plot the data
f, ax = plt.subplots(figsize=(10, 4))
cali_seasonal_mean.plot(marker="o",
                        color="grey",
                        markerfacecolor="purple",
                        markeredgecolor="purple")
ax.set(title="Seasonal Mean Temperature")
plt.show()


#%% #################

# Export Seasonal Climate Project Data To .csv File
# At this point you can convert the data to a dataframe and export it to a .csv format if you wish.

# Convert to a dataframe
cali_seasonal_mean_df = cali_seasonal_mean.to_dataframe()
cali_seasonal_mean_df



#%% #################

# Export a csv file
cali_seasonal_mean_df.to_csv("cali-seasonal-temp.csv")



#%% #################

# Plot Seasonal Data By Season
# Using groupby() you can group the data and plot it by season to better look at seasonal trends.

colors = {3: "grey", 6: "lightgreen", 9: "green", 12: "purple"}
seasons = {3: "spring", 6: "summer", 9: "fall", 12: "winter"}

f, ax = plt.subplots(figsize=(10, 7))
for month, arr in cali_seasonal_mean.groupby('time.month'):
    arr.plot(ax=ax,
             color="grey",
             marker="o",
             markerfacecolor=colors[month],
             markeredgecolor=colors[month],
             label=seasons[month])

ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax.set(title="Seasonal Change in Mean Temperature Over Time")
plt.show()



#%% #################

# Weighted Summary by Season
# To begin, you will generate a list of days in each month which will be used to weight your 
# seasonal summary data according to the the days in each month.
# TODO – redo this section to use the approach above which is perfect

# Calculate seasonal averages
# http://xarray.pydata.org/en/stable/examples/monthly-means.html

month_length = cali_temp_masked.time.dt.days_in_month
month_length


#%% #################

# Next, divide the data grouped by season by the total days represented in each season to create weighted values

# This is returning values of 0 rather than na
# Calculate a weighted mean by season
cali_weighted_mean = ((cali_temp * month_length).resample(time='QS-DEC').sum() /
                      month_length.resample(time='QS-DEC').sum())
# Replace 0 values with nan
cali_weighted_mean = cali_weighted_mean.where(cali_weighted_mean)
cali_weighted_mean.shape


#%% #################

cali_weighted_season_value = cali_weighted_mean.groupby('time').mean([
    "lat", "lon"])
cali_weighted_season_value.shape


#%% #################

colors = {3: "grey", 6: "lightgreen", 9: "green", 12: "purple"}
seasons = {3: "Spring", 6: "Summer", 9: "Fall", 12: "Winter"}

f, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharey=True)
for month, arr in cali_weighted_season_value.groupby('time.month'):
    arr.plot(ax=ax1,
             color="grey",
             marker="o",
             markerfacecolor=colors[month],
             markeredgecolor=colors[month],
             label=seasons[month])

ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.set(title="Weighted Seasonal Change in Mean Temperature Over Time")

for month, arr in cali_seasonal_mean.groupby('time.month'):
    arr.plot(ax=ax2,
             color="grey",
             marker="o",
             markerfacecolor=colors[month],
             markeredgecolor=colors[month],
             label=seasons[month])

ax2.set(title="Unweighted Seasonal Change in Mean Temperature Over Time")
f.tight_layout()
plt.show()



#%% #################

# If you want, you can compare the difference between weighted vs unweighted values.

# What does the difference look like weighted vs unweighted?
cali_seasonal_mean - cali_weighted_season_value


#%% #################

# The Same Analysis for the West Coast
# Above you calculate seasonal summaries for the state of California. You can implement the same analysis 
# for each aoi region in a shapefile if you want following the workflow that you learned in the previous lesson.


# Create AOI Subset
cali_or_wash_nev = states_gdf[states_gdf.name.isin(
    ["California", "Oregon", "Washington", "Nevada"])]
west_bounds = get_aoi(cali_or_wash_nev)

# Create the mask
west_mask = regionmask.mask_3D_geopandas(cali_or_wash_nev,
                                         monthly_forecast_temp_xr.lon,
                                         monthly_forecast_temp_xr.lat)


# Slice by time & aoi location
start_date = "2059-12-15"
end_date = "2099-12-15"

west_temp = monthly_forecast_temp_xr["air_temperature"].sel(
    time=slice(start_date, end_date),
    lon=slice(west_bounds["lon"][0], west_bounds["lon"][1]),
    lat=slice(west_bounds["lat"][0], west_bounds["lat"][1]))

# Apply the mask
west_temp_masked = west_temp.where(west_mask)
west_temp_masked
# Resample the data by season across all years
#west_season_mean_all_years = west_temp_masked.groupby('region').resample(time='QS-DEC', keep_attrs=True).mean()
# cali_seasonal_mean = cali_season_mean_all_years.groupby('time').mean(["lat", "lon"])
# cali_seasonal_mean



#%% #################


# This produces a raster for each season over time across regions
west_coast_mean_temp_raster = west_temp_masked.resample(
    time='QS-DEC', keep_attrs=True).mean()
west_coast_mean_temp_raster.shape



#%% #################


# This produces a regional summary
regional_summary = west_coast_mean_temp_raster.groupby('time').mean([
    "lat", "lon"])
regional_summary.plot(col="region",
                      marker="o",
                      color="grey",
                      markerfacecolor="purple",
                      markeredgecolor="purple",
                      col_wrap=2,
                      figsize=(12, 8))

plt.suptitle("Seasonal Temperature by Region", y=1.03)
plt.show()



#%% #################


# The data can then be easily converted to a dataframe
regional_summary.to_dataframe()



#%% #################




#%% #################




