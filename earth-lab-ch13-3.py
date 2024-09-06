#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep  3, 2024

Lesson 3. How to Download MACA2 Climate Data Using Python

from: https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/get-maca-2-climate-data-netcdf-python/

@author: bblrd
"""

# Import packages
import numpy as np
import netCDF4
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns

#%% #################

# Plotting options
sns.set(font_scale=1.3)
sns.set_style("white")

# Models to chose from
"""
model_name = ('bcc-csm1-1',
              'bcc-csm1-1-m',
              'BNU-ESM',
              'CanESM2',
              'CCSM4',
              'CNRM-CM5',
              'CSIRO-Mk3-6-0',
              'GFDL-ESM2G',
              'GFDL-ESM2M',
              'HadGEM2-CC365',
              'HadGEM2-ES365',
              'inmcm4',
              'IPSL-CM5A-MR',
              'IPSL-CM5A-LR',
              'IPSL-CM5B-LR',
              'MIROC5',
              'MIROC-ESM',
              'MIROC-ESM-CHEM',
              'MRI-CGCM3',
              'NorESM1-M')

model =  This Python variable can be set to any number between 0 and 19 which represents the 20 climate models 
that are available for MACA v2 data. The model represents how (the methods used) the climate data were created. 
You can learn more about each model by clicking here

"""

# # These are the variable options for the met data
"""
variable_name = ('tasmax',
                 'tasmin',
                 'rhsmax',
                 'rhsmin',
                 'pr',
                 'rsds',
                 'uas',
                 'vas',
                 'huss')

var =  is the variable in the dataset you want to work with. There are 9 options for variables and 
they are listed in both short and long name versions below. You can assign var =  to any number 
between 0 and 8, where 0 is the first option in the list, and 8 is the last. In the list below note 
that is var = 0 you would be selecting tax_max or max temperature.

"""

# These are var options in long form
"""
# These are var options in long form
var_long_name = ('air_temperature',
                 'air_temperature',
                 'relative_humidity',
                 'relative_humidity',
                 'precipitation',
                 'surface_downwelling_shortwave_flux_in_air',
                 'eastward_wind',
                 'northward_wind',
                 'specific_humidity')
"""

# Climate Data Scenarios
"""
scenario =  can be chosen to pick which climate scenario you want to you. 0 is the historical actual data. 
This data is based on actual data and is not modeled. 1 is the rcp45 scenario, which is described as an 
intermediate climate scenario. 2 is the rcp85 scenario, which is a worst case (strongest immissions) 
climate scenario.
"""


#%% #################

# Select Data Download Options
# Below you first create lists containing the the options that you wish to use to download your data.

# This is the base url required to download data from the thredds server.
dir_path = 'http://thredds.northwestknowledge.net:8080/thredds/dodsC/'

# These are the variable options for the met data
variable_name = ('tasmax',
                 'tasmin',
                 'rhsmax',
                 'rhsmin',
                 'pr',
                 'rsds',
                 'uas',
                 'vas',
                 'huss')

# These are var options in long form
var_long_name = ('air_temperature',
                 'air_temperature',
                 'relative_humidity',
                 'relative_humidity',
                 'precipitation',
                 'surface_downwelling_shortwave_flux_in_air',
                 'eastward_wind',
                 'northward_wind',
                 'specific_humidity')

# Models to chose from
model_name = ('bcc-csm1-1',
              'bcc-csm1-1-m',
              'BNU-ESM',
              'CanESM2',
              'CCSM4',
              'CNRM-CM5',
              'CSIRO-Mk3-6-0',
              'GFDL-ESM2G',
              'GFDL-ESM2M',
              'HadGEM2-CC365',
              'HadGEM2-ES365',
              'inmcm4',
              'IPSL-CM5A-MR',
              'IPSL-CM5A-LR',
              'IPSL-CM5B-LR',
              'MIROC5',
              'MIROC-ESM',
              'MIROC-ESM-CHEM',
              'MRI-CGCM3',
              'NorESM1-M')

# Scenarios
scenario_type = ('historical', 'rcp45', 'rcp85')

# Year start and ends (historical vs projected)
year_start = ('1950', '2006', '2006')
year_end = ('2005', '2099', '2099')
run_num = [1] * 20
run_num[4] = 6  # setting CCSM4 with run 6
domain = 'CONUS'


#%% #################

# Next, select the options that you want to use for your data download.

# Model options between 0-19
model = 2
# Options 0-8 will work for var. Var maps to the variable name below
var = 0
# Options range from 0-2
scenario = 2

try: 
    print("Great! You have selected: \n \u2705 Variable: {} \n \u2705 Model: {}, "
      "\n \u2705 Scenario: {}".format(variable_name[var], 
                                      model_name[model],
                                      scenario_type[scenario]))
except IndexError as e:
    raise IndexError("Oops, it looks like you selected value that is "
                     "not within the range of values which is 0-2. please look"
                     "closely at your selected values.")

# Great! You have selected: 
# Variable: tasmax 
# Model: BNU-ESM, 
# Scenario: rcp85

#%% #################

# Finally, use the scenario variable to select the time period associated with the options selected above.

try:
    time = year_start[scenario]+'_' + year_end[scenario]
    print("\u2705 Your selected time period is:", time)
except IndexError as e:
    raise IndexError("Oops, it looks like you selected a scenario value that is \
                     not within the range of values which is 0-2")
    

# Your selected time period is: 2006_2099



#%% #################










#%% #################














#%% #################





















