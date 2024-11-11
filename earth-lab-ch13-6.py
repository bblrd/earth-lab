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



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################



#%% #################





