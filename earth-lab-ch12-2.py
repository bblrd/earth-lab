#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Apr 2, 2025

Lesson 2. Open and Use MODIS Data in HDF4 format in Open Source Python

from: https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/open-MODIS-hdf4-files-python/

@author: bblrd
"""

# Import packages
import os
import warnings

import matplotlib.pyplot as plt
import numpy.ma as ma
import xarray as xr
import rioxarray as rxr
from shapely.geometry import mapping, box
import geopandas as gpd
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

warnings.simplefilter('ignore')

# Get the MODIS data
et.data.get_data('cold-springs-modis-h4')

# This download contains the fire boundary
et.data.get_data('cold-springs-fire')

# Set working directory
os.chdir(os.path.join(et.io.HOME,
                      'earth-analytics',
                      'data'))
# Downloading from https://ndownloader.figshare.com/files/10960112
# Extracted output to /root/earth-analytics/data/cold-springs-modis-h4/.

#%% #################

# Create a path to the pre-fire MODIS h4 data
modis_pre_path = os.path.join("cold-springs-modis-h4",
                              "07_july_2016",
                              "MOD09GA.A2016189.h09v05.006.2016191073856.hdf")
modis_pre_path
'cold-springs-modis-h4/07_july_2016/MOD09GA.A2016189.h09v05.006.2016191073856.hdf'


#%% #################

# Open data with rioxarray
modis_pre = rxr.open_rasterio(modis_pre_path,
                              masked=True)
type(modis_pre)


#%% #################

# This is just a data exploration step
modis_pre_qa = modis_pre[0]
modis_pre_qa


#%% #################

modis_pre_qa["num_observations_1km"]


#%% #################

# Reflectance data
modis_pre_bands = modis_pre[1]
modis_pre_bands


#%% #################

# Use rasterio to print all of the subdataset names in the data
# Here you can see the group names: MODIS_Grid_500m_2D & MODIS_Grid_1km_2D
import rasterio as rio
with rio.open(modis_pre_path) as groups:
    for name in groups.subdatasets:
        print(name)

#%% #################

# Subset by group only - Notice you have all bands in the returned object
rxr.open_rasterio(modis_pre_path,
                  masked=True,
                  group="MODS_Grid_500m_2D").squeeze()

#%% #################

# Open just the bands that you want to process
desired_bands = ["sur_refl_b01_1",
                 "sur_refl_b02_1",
                 "sur_refl_b03_1",
                 "sur_refl_b04_1",
                 "sur_refl_b07_1"]
# Notice that here, you get a single xarray object with just the bands that
# you want to work with
modis_pre_bands = rxr.open_rasterio(modis_pre_path,
                                    variable=desired_bands).squeeze()
modis_pre_bands

#%% #################

#  view nodata value
modis_pre_bands.sur_refl_b01_1.rio.nodata

#%% #################

# Open just the bands that you want to process
desired_bands = ["sur_refl_b01_1",
                 "sur_refl_b02_1",
                 "sur_refl_b03_1",
                 "sur_refl_b04_1",
                 "sur_refl_b07_1"]
# Notice that here, you get a single xarray object with just the bands that
# you want to work with
modis_pre_bands = rxr.open_rasterio(modis_pre_path,
                                    masked=True,
                                    variable=desired_bands).squeeze()
modis_pre_bands

#%% #################

# Now your nodata value returns a NAN as it has been masked
# and accounted for
modis_pre_bands.sur_refl_b01_1.rio.nodata

#%% #################

# Plot band one of the data
ep.plot_bands(modis_pre_bands.sur_refl_b01_1)
plt.show()

#%% #################

# Note that you can also call the data variable by name
ep.plot_bands(modis_pre_bands["sur_refl_b01_1"])
plt.show()

#%% #################

# Plot All MODIS Bands with EarthPy
# Now that you have the needed reflectance data, you can plot your data using earthpy.plot_bands.
# To plot all bands in the data, you will need to first create an Xarray DataArray object.

print(type(modis_pre_bands))
print(type(modis_pre_bands.to_array()))

# You can plot each band easily using a data array object
modis_pre_bands.to_array()

#%% #################

# Plot the data as a DataArray
# This is only a data exploration step
ep.plot_bands(modis_pre_bands.to_array().values,
              figsize=(10, 6))
plt.show()

#%% #################

# Select the rgb bands only
rgb_bands = ['sur_refl_b01_1',
             'sur_refl_b03_1',
             'sur_refl_b04_1']
# Turn the data into a DataArray
modis_rgb_xr = modis_pre_bands[rgb_bands].to_array()
modis_rgb_xr

#%% #################

# Plot MODIS RGB numpy image array
ep.plot_rgb(modis_rgb_xr.values,
            rgb=[0, 2, 1],
            title='RGB Image of MODIS Data')

plt.show()

#%% #################

# Crop (Clip) MODIS Data Using Rioxarray
# Above you opened and plotted MODIS reflectance data. However, the data cover a larger study area than you need. 
# It is a good idea to crop your the data to maximize processing efficiency. Less pixels means less processing time and power needed

# Open fire boundary
fire_boundary_path = os.path.join("cold-springs-fire",
                                  "vector_layers",
                                  "fire-boundary-geomac",
                                  "co_cold_springs_20160711_2200_dd83.shp")

fire_boundary = gpd.read_file(fire_boundary_path)

# Check the CRS of your study area extent
fire_boundary.crs

#%% #################

# Check CRS
if not fire_boundary.crs == modis_rgb_xr.rio.crs:
    # If the crs is not equal reproject the data
    fire_bound_sin = fire_boundary.to_crs(modis_rgb_xr.rio.crs)

fire_bound_sin.crs

#%% #################

#%% #################

#%% #################

#%% #################

#%% #################


