#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep  2, 2024

Lesson 1. Introduction to the NetCDF4 Hierarchical Data Format

from: https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/intro-to-climate-data/

@author: bblrd
"""

# What is netCDF Data?

"""
NetCDF (network Common Data Form) is a hierarchical data format similar to hdf4 and hdf5. It is what is 
known as a “self-describing” data structure which means that metadata, or descriptions of the data, are 
included in the file itself and can be parsed programmatically, meaning that they can be accessed using 
code to build automated and reproducible workflows.

The NetCDF format can store data with multiple dimensions. It can also store different types of data through 
arrays that can contain geospatial imagery, rasters, terrain data, climate data, and text. These arrays support 
metadata, making the netCDF format highly flexible. NetCDF was developed and is supported by UCAR who maintains 
standards and software that support the use of the format.

NetCDF4 Format for Climate Data
The hierarchical and flexible nature of netcdf files supports storing data in many different ways. This 
flexibility is nice, however, similar to hdf5 data formats, it can be challenging when communities make 
different decisions about how and where they store data in a netCDF file. The netCDF4 data standard is used 
broadly by the climate science community to store climate data. Climate data are:

-often delivered in a time series format (months and years of historic or future projected data).
-spatial in nature, covering regions such as the United States or even the world.
-driven by models which require documentation making the self describing aspect of netCDF files useful.

The netCDF4 format supports data stored in an array format. Arrays are used to store raster spatial data 
(terrain layers, gridded temperature data, etc) and also point based time series data (for example temperature 
for a single location over 10 years). Climate data typically have three dimensions—x and y values representing 
latitude and longitude location for a point or a grid cell location on the earth’s surface and time.

The x/y locations often store a data value such as temperature, humidity, precipitation or wind direction.

NetCDF is Self Describing
One of the biggest benefits of working with a data type like netCDF is that it is self-describing. This means that all of the metadata needed to work with the data is often contained within the netCDF file (the .nc file) itself.
"""

# Tools to Work With NetCDF Data

"""
Python also has several open source tools that are useful for processing netcdf files including:

-Xarray: one of the most common tools used to process netcdf data. Xarray knows how to open netcdf 4 
files automatically giving you access to the data and metadata in spatial formats.
-rioxarray: a wrapper that adds spatial functionality such as reproject and export to geotiff to xarray objects.
-Regionmask: regionmask builds on top of xarray to support spatial subsetting and AOIs for xarray objects.
In the next lessons you will learn more about climate data and how to open climate data stored in netCDF 
format using open source Python tools. Read the section below to learn more about the climate data itself.
"""








