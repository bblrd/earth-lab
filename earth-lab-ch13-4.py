#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 16, 2024

Lesson 4. How to Open and Process NetCDF 4 Data Format in Open Source Python

from: https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/use-netcdf-in-python-xarray/

@author: bblrd
"""

# netCDF4 needs to be installed in your environment for this to work
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import earthpy as et

# Plotting options
sns.set(font_scale=1.3)
sns.set_style("white")

# Optional - set your working directory if you wish to use the data
# accessed lower down in this notebook (the USA state boundary data)
#os.chdir(os.path.join(et.io.HOME,
#                      'earth-analytics',
#                      'data'))

#%% #################

# The (online) url for a MACAv2 dataset for max monthly temperature
data_path = "http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_macav2metdata_tasmax_BNU-ESM_r1i1p1_historical_1950_2005_CONUS_monthly.nc"

max_temp_xr  = xr.open_dataset(data_path)  
# View xarray object
max_temp_xr



#%% #################

# For later - grab the crs of the data using rioxarray
climate_crs = max_temp_xr.rio.crs
climate_crs




#%% #################


# View first 5 latitude values
max_temp_xr["air_temperature"]["lat"].values[:5]

print("The min and max latitude values in the data is:", 
      max_temp_xr["air_temperature"]["lat"].values.min(), 
      max_temp_xr["air_temperature"]["lat"].values.max())
print("The min and max longitude values in the data is:", 
      max_temp_xr["air_temperature"]["lon"].values.min(), 
      max_temp_xr["air_temperature"]["lon"].values.max())




#%% #################


# View first 5 and last. 5 time values - notice the span of
# dates range from 1950 to 2005
print("The earliest date in the data is:", max_temp_xr["air_temperature"]["time"].values.min())
print("The latest date in the data is:", max_temp_xr["air_temperature"]["time"].values.max())  



#%% #################


max_temp_xr["air_temperature"]["time"].values.shape



#%% #################


# View metadata
metadata = max_temp_xr.attrs
metadata



#%% #################


# View data title
metadata["title"]



#%% #################


# Select a single x,y combination from the data
key=400
longitude = max_temp_xr["air_temperature"]["lon"].values[key]
latitude = max_temp_xr["air_temperature"]["lat"].values[key]

print("Long, Lat values:", longitude, latitude)



#%% #################



# Create a spatial map of your selected location with cartopy

# Set the spatial extent to cover the CONUS (Continental United States)
extent = [-120, -70, 24, 50.5]
central_lon = np.mean(extent[:2])
central_lat = np.mean(extent[2:])

# Create your figure and axis object
# Albers equal area is a common CRS used to make maps of the United States
f, ax = plt.subplots(figsize=(12, 6),
                     subplot_kw={'projection': ccrs.AlbersEqualArea(central_lon, central_lat)})
ax.coastlines()
# Plot the selected location
ax.plot(longitude-360, latitude, 
        '*', 
        transform=ccrs.PlateCarree(),
        color="purple", 
        markersize=10)

ax.set_extent(extent)
ax.set(title="Location of the Latitude / Longitude Being Used To to Slice Your netcdf Climate Data File")

# Adds continent boundaries to the map
ax.add_feature(cfeature.LAND, edgecolor='black')

ax.gridlines()
plt.show()



#%% #################


# Slice the data spatially using a single lat/lon point
one_point = max_temp_xr["air_temperature"].sel(lat=latitude,
                                               lon=longitude)
one_point




#%% #################



# Notice the shape of the output array
one_point.shape



#%% #################

# View the first 5 values for that single point
one_point.values[:5]




#%% #################


# Use xarray to create a quick time series plot
one_point.plot.line()
plt.show()



#%% #################

# You can clean up your plot as you wish using standard matplotlib approaches
f, ax = plt.subplots(figsize=(12, 6))
one_point.plot.line(hue='lat',
                    marker="o",
                    ax=ax,
                    color="grey",
                    markerfacecolor="purple",
                    markeredgecolor="purple")
ax.set(title="Time Series For a Single Lat / Lon Location")

# Uncomment the line below if you wish to export the figure as a .png file
# plt.savefig("single_point_timeseries.png")
plt.show()



#%% #################


# Convert to dataframe -- then this can easily be exported to a csv
one_point_df = one_point.to_dataframe()
# View just the first 5 rows of the data
one_point_df.head()



#%% #################


# Export data to .csv file
one_point_df.to_csv("one-location.csv")



#%% #################


start_date = "2000-01-01"
end_date = "2005-01-01"
temp_2000_2005 = max_temp_xr["air_temperature"].sel(time=slice(start_date, end_date),
                                                    lat=45.02109146118164,
                                                    lon=243.01937866210938)
temp_2000_2005



#%% #################


temp_2000_2005.shape



#%% #################


# View the 60 data points (raster cell values) associated with the spatial and temporal subset
temp_2000_2005.values


#%% #################


# Plot the data just like you did above
f, ax = plt.subplots(figsize=(12, 6))
temp_2000_2005.plot.line(hue='lat',
                         marker="o",
                         ax=ax,
                         color="grey",
                         markerfacecolor="purple",
                         markeredgecolor="purple")
ax.set(title="A 5 Year Time Series of Temperature Data For A Single Location")
plt.show()



#%% #################

# Convert to dataframe -- then this can be exported to a csv if you want that
temp_2000_2005_df = temp_2000_2005.to_dataframe()
# View just the first 5 rows of the data
temp_2000_2005_df.head()


#%% #################

# Create filename from subset info
file_name = "monthly-temp-" + start_date + "-" + end_date + ".csv"
file_name


#%% #################


# Export to a csv file to share with your friends!
temp_2000_2005_df.to_csv(file_name)


#%% #################

start_date = "1950-01-15"
end_date = "1950-02-15"

two_months_conus = max_temp_xr["air_temperature"].sel(
    time=slice(start_date, end_date))
# Notice that time has a value of **2** below representing two time steps or months worth of data
two_months_conus


#%% #################

two_months_conus.shape


#%% #################

# Directly plot just a single day using time in "years"
two_months_conus.plot()
plt.show()


#%% #################

# Quickly plot the data using xarray.plot()
two_months_conus.plot(x="lon",
                      y="lat",
                      col="time",
                      col_wrap=1)
plt.suptitle("Two Time Steps of Monthly Average Temp", y=1.03)
plt.show()


#%% #################

# Plot the data using 2 columns
two_months_conus.plot(x="lon",
                      y="lat",
                      col="time",
                      col_wrap=2)
plt.show()


#%% #################

central_lat = 37.5
central_long = 96
extent = [-120, -70, 20, 55.5]  # CONUS

map_proj = ccrs.AlbersEqualArea(central_longitude=central_lon,
                                central_latitude=central_lat)

aspect = two_months_conus.shape[2] / two_months_conus.shape[1]
p = two_months_conus.plot(transform=ccrs.PlateCarree(),  # the data's projection
                          col='time', col_wrap=1,
                          aspect=aspect,
                          figsize=(10, 10),
                          subplot_kws={'projection': map_proj})  # the plot's projection

plt.suptitle("Two Time Steps of CONUS Historic Temperature Data", y=1)
# Add the coastlines to each axis object and set extent
for ax in p.axes.flat:
    ax.coastlines()
    ax.set_extent(extent)


#%% #################

# Double check the crs still exist
two_months_conus.rio.crs


#%% #################

# Export to geotiff
file_path = "two_months_temp_data.tif"
two_months_conus.rio.to_raster(file_path)


#%% #################


# Open the data up as a geotiff
two_months_tiff = rxr.open_rasterio(file_path)
two_months_tiff


#%% #################


two_months_tiff.plot()
plt.show()


#%% #################


# Plot the data - this doesn't look right!
two_months_tiff.plot(col="band")
plt.show()


#%% #################


two_months_tiff.rio.nodata


#%% #################


# Remove no data values and try to plot again
two_months_tiff = rxr.open_rasterio(file_path)

two_months_clean = two_months_tiff.where(
    two_months_tiff != two_months_tiff.rio.nodata)

two_months_clean.plot(col="band")
plt.show()


#%% #################





