#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep  3, 2024

Lesson 2. Introduction to the CMIP and MACA v2 Climate Data

from : https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/intro-to-MACAv2-cmip5-data/

@author: bblrd
"""


# About Climate Data: What is CMIP5 data?
"""
About Climate Data: What is CMIP5 data?
The Climate Model Intercomparison Project, better known as CMIP, is a framework for analyzing and 
comparing Global Climate Models (GCMs) to better understand climate change occuring now and into the future. 
GCMs are a type of climate models that simulate the global and regional scale climate processes that include 
the general circulation of atmosphere and oceans and its interaction with the land, radiative fluxes, 
cloud processes, and land surface processes that include hydrology and biological feedbacks. CMIP5, phase 5 
of the project, is the current and most extensive CMIP, drawing data from over 40 GCMs from countries around 
the world.
"""

# What is MACA v2 Metdata?
"""
The CMIP models are global and thus cover the entire world. Due to this global coverage they are delivered
at a coarse resolution ranging from 100-300km. Multivariate Adaptive Constructed Analogs (MACA) is a statistical 
method for downscaling GCM data from its coarse format to a higher spatial resolution for the Continental United
States (CONUS). The MACA downscaling approach takes 20 GCMs from CMIP5 and downscales them to 4km or 6km 
resolution data. The resolution of MACA v2 Metdata is 4km.

The data variables include temperature, precipitation, humidity, downward shortwave solar radiation, 
and eastward and northward wind. Data are also provided for historical time periods from 1950-2005 
and future scenarios spanning from 2006-2100.
"""

# About Downscaling Data
"""
Creating Higher Resolution Climate Data For the United States Using Lower Resolution Global Data
Downscaling refers to the process of taking climate projections data produced at a large scale, 
with bigger pixels covering larger areas (100-300 km), and increasing its spatial resolution so 
that the pixels are smaller and cover smaller areas (1-50 km). Downscaling processes also generally 
tend to remove biases (often referred to as bias correction) between the simulated GCM climatology 
and the real world climatology. Downscaling allows us to have future climate projections available 
at a much finer spatial scale and more representative of a region’s climate and therefore more 
applicable for regional-scale applications. For example, it is more appropriate for discerning 
projected hydrological changes at a watershed scale as opposed to taking those projections directly 
from a GCM output. Overall, downscaling makes the data more useful on a local and regional level, which 
is important because adaptation strategies are generally identified and implemented on regional and local 
scales. This allows resource managers to identify vulnerable areas and prioritize adaptation efforts there.
"""

# What Formats Are MACA v2 Data In?
"""
Tabular (txt and csv) - Learn how to work with txt and csv data in this lesson.
GeoTIFF - Learn how to work with geotiff data in this lesson.
netCDF - Get more detail on the netCDF documentation from UCAR here.

"""










