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



#%% #################



#%% #################



#%% #################



#%% #################






