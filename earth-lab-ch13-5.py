#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep  11, 2024

Lesson 5. Calculate Summary Values Using Spatial Areas of Interest (AOIs) 
including Shapefiles for Climate Data Variables Stored in NetCDF 4 Format: 
Work With MACA v2 Climate Data in Python

from: https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/subset-netcdf4-climate-data-spatially-aoi/

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

# Spatial subsetting of netcdf files
import regionmask

# Plotting options
sns.set(font_scale=1.3)
sns.set_style("white")

# Optional - set your working directory if you wish to use the data
# accessed lower down in this notebook (the USA state boundary data)
os.chdir(os.path.join(et.io.HOME, 'earth-analytics', 'data'))


#%% #################

# Get netcdf file
data_path_monthly = 'http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_macav2metdata_tasmax_BNU-ESM_r1i1p1_rcp45_2006_2099_CONUS_monthly.nc'

# Open up the data
with xr.open_dataset(data_path_monthly) as file_nc:
    monthly_forecast_temp_xr = file_nc

# View xarray object
monthly_forecast_temp_xr






#%% #################


# Download natural earth data which contains state boundaries to generate AOI
url =  (
    "https://naturalearth.s3.amazonaws.com/"
    "50m_cultural/ne_50m_admin_1_states_provinces_lakes.zip"
)
states_gdf = gpd.read_file(url)
states_gdf.head()







#%% #################



# You will use the bounds to determine the slice values for this data
# Select any state in the CONUS that you wish here! California is the default
cali_aoi = states_gdf[states_gdf.name == "California"]
# Get the total spatial extent for California
cali_aoi.total_bounds









#%% #################




# Get lat min, max
aoi_lat = [float(cali_aoi.total_bounds[1]), float(cali_aoi.total_bounds[3])]
aoi_lon = [float(cali_aoi.total_bounds[0]), float(cali_aoi.total_bounds[2])]
# Notice that the longitude values have negative numbers
# we need these values in a global crs so we can subtract from 360
aoi_lat, aoi_lon










#%% #################





# The netcdf files use a global lat/lon so adjust values accordingly
aoi_lon[0] = aoi_lon[0] + 360
aoi_lon[1] = aoi_lon[1] + 360
aoi_lon






#%% #################


# Slice the data by time and spatial extent
start_date = "2010-01-15"
end_date = "2010-02-15"

two_months_cali = monthly_forecast_temp_xr["air_temperature"].sel(
    time=slice(start_date, end_date),
    lon=slice(aoi_lon[0], aoi_lon[1]),
    lat=slice(aoi_lat[0], aoi_lat[1]))
two_months_cali





#%% #################


# Plot a quick histogram
two_months_cali.plot()
plt.show()






#%% #################




# Spatial Plot for the selected AOI (California)
two_months_cali.plot(col='time',
                     col_wrap=1)

plt.show()






#%% #################



# Only subset by location / not time
cali_ts = monthly_forecast_temp_xr["air_temperature"].sel(
    lon=slice(aoi_lon[0], aoi_lon[1]),
    lat=slice(aoi_lat[0], aoi_lat[1]))
cali_ts






#%% #################



# Time series plot of max temperature per year. for California
# You will get a RuntimeWarning warning here because of nan values...
# This is the max value in each pixel across all months for each year
cali_annual_max = cali_ts.groupby('time.year').max(skipna=True)
cali_annual_max






#%% #################




cali_annual_max_val = cali_annual_max.groupby("year").max(["lat", "lon"])
cali_annual_max_val







#%% #################



# Plot the data
f, ax = plt.subplots(figsize=(12, 6))
cali_annual_max_val.plot.line(hue='lat',
                              marker="o",
                              ax=ax,
                              color="grey",
                              markerfacecolor="purple",
                              markeredgecolor="purple")
ax.set(title="Annual Max Temperature (K) in California")
plt.show()









#%% #################




# This is the AOI of interest. You only want to calculate summary values for
# pixels within this AOI rather the entire rectangular spatial extent.
f, ax = plt.subplots()
cali_aoi.plot(ax=ax)
ax.set(title="California AOI Subset")

plt.show()








#%% #################


cali_aoi








#%% #################


# Create a 3d mask - this contains the true / false values identifying pixels
# inside vs outside of the mask region
cali_mask = regionmask.mask_3D_geopandas(cali_aoi,
                                         monthly_forecast_temp_xr.lon,
                                         monthly_forecast_temp_xr.lat)
cali_mask









#%% #################




# Slice out two months of data
two_months = monthly_forecast_temp_xr.sel(
    time=slice('2099-10-25', '2099-12-15'))








#%% #################



# Apply the mask for California to the data
two_months = two_months.where(cali_mask)
two_months









#%% #################






two_months["air_temperature"].plot(col='time',
                                   col_wrap=1,
                                   figsize=(10, 10))
plt.show()





#%% #################


two_months_masked = monthly_forecast_temp_xr["air_temperature"].sel(time=slice('2099-10-25',
                                                                               '2099-12-15'),
                                                                    lon=slice(aoi_lon[0],
                                                                              aoi_lon[1]),
                                                                    lat=slice(aoi_lat[0],
                                                                              aoi_lat[1])).where(cali_mask)
two_months_masked.dims










#%% #################



# Start by extracting a few states from the states_gdf
states_gdf["name"]

cali_or_wash_nev = states_gdf[states_gdf.name.isin(
    ["California", "Oregon", "Washington", "Nevada"])]
cali_or_wash_nev.plot()
plt.show()







#%% #################



west_mask = regionmask.mask_3D_geopandas(cali_or_wash_nev,
                                         monthly_forecast_temp_xr.lon,
                                         monthly_forecast_temp_xr.lat)
west_mask










#%% #################



def get_aoi(shp, world=True):
    """Takes a geopandas object and converts it to a lat/ lon
    extent 

    Parameters
    -----------
    shp : GeoPandas GeoDataFrame
        A geodataframe containing the spatial boundary of interest
    world : boolean
        True if you want lat / long to represent sinusoidal (0-360 degrees)

    Returns
    -------
    Dictionary of lat and lon spatial bounds
    """

    lon_lat = {}
    # Get lat min, max
    aoi_lat = [float(shp.total_bounds[1]), float(shp.total_bounds[3])]
    aoi_lon = [float(shp.total_bounds[0]), float(shp.total_bounds[2])]

    if world:
        aoi_lon[0] = aoi_lon[0] + 360
        aoi_lon[1] = aoi_lon[1] + 360
    lon_lat["lon"] = aoi_lon
    lon_lat["lat"] = aoi_lat
    return lon_lat


west_bounds = get_aoi(cali_or_wash_nev)









#%% #################


# Slice the data
start_date = "2010-01-15"
end_date = "2010-02-15"

# Subset
two_months_west_coast = monthly_forecast_temp_xr["air_temperature"].sel(
    time=slice(start_date, end_date),
    lon=slice(west_bounds["lon"][0], west_bounds["lon"][1]),
    lat=slice(west_bounds["lat"][0], west_bounds["lat"][1]))
two_months_west_coast









#%% #################



two_months_west_coast.plot(col="time",
                           col_wrap=1,
                           figsize=(5, 8))
plt.show()












#%% #################



# Apply the mask for the west coast subset
two_months_west_coast = two_months_west_coast.where(west_mask)
two_months_west_coast.dims













#%% #################





cali_or_wash_nev









#%% #################




# Note that the region values align with the index of the geodataframe above
two_months_west_coast.region










#%% #################




two_months_west_coast.plot(col="time",
                           row="region",
                           sharey=False, sharex=False)
plt.show()






#%% #################






summary = two_months_west_coast.groupby("time").mean(["lat", "lon"])
summary.to_dataframe()





#%% #################


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

# Here is the entire workflow from start to end

url =  (
    "https://naturalearth.s3.amazonaws.com/"
    "50m_cultural/ne_50m_admin_1_states_provinces_lakes.zip"
)
states_gdf = gpd.read_file(url)


# Get netcdf file
data_path_monthly = 'http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_macav2metdata_tasmax_BNU-ESM_r1i1p1_rcp45_2006_2099_CONUS_monthly.nc'

# Open up the data
with xr.open_dataset(data_path_monthly) as file_nc:
    monthly_forecast_temp_xr = file_nc

# View xarray object
monthly_forecast_temp_xr

# Start by extracting a few states from the states_gdf
# I am using this as a shapefile because i presume some of my students
# will want to use custom aoi's so i want to teach using a shapefil rather than
# the regionmask built in shapes as nice as they are :)
states_gdf["name"]

cali_or_wash_nev = states_gdf[states_gdf.name.isin(
    ["California", "Oregon", "Washington", "Nevada"])]

west_mask = regionmask.mask_3D_geopandas(cali_or_wash_nev,
                                         monthly_forecast_temp_xr.lon,
                                         monthly_forecast_temp_xr.lat)
west_mask


west_bounds = get_aoi(cali_or_wash_nev)


# Slice the data
start_date = "2010-01-15"
end_date = "2020-02-15"

# Subset the data - this is now a dataarray rather than a DataSet
two_months_west_coast = monthly_forecast_temp_xr["air_temperature"].sel(
    time=slice(start_date, end_date),
    lon=slice(west_bounds["lon"][0], west_bounds["lon"][1]),
    lat=slice(west_bounds["lat"][0], west_bounds["lat"][1])).where(west_mask)

# This output is a dataarray
two_months_west_coast

# Plot the data - this produces a single histogram
two_months_west_coast.plot()
plt.show()



#%% #################

# Keep in mind that as you add more data to your slice, the processing will slow down.
regional_summary = two_months_west_coast.groupby("region").mean(["lat", "lon"])
regional_summary.plot(col="region",
                      marker="o",
                      color="grey",
                      markerfacecolor="purple",
                      markeredgecolor="purple",
                      col_wrap=2)
plt.show()


#%% #################

two_months_west_coast.groupby("region").mean(["lat", "lon"]).to_dataframe()



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################





