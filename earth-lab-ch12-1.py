#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar  30, 2025

Lesson 1. Introduction to the HDF4 Data Format - Explore H4 Files Using HDFView

from: https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/intro-to-hdf4/

@author: bblrd
"""

# What are HDF4 Files?

"""
On the landing page of this section, you learned about the general characteristics
 of Hierarchical Data Format (HDF) files and that there are many types of HDF files
 including HDF4, HDF5, and NetCDF. HDF files are open source file formats that support
 large, complex, heterogeneous data, using a “file directory” like structure. HDF 
 formats also allow for embedding of metadata, making them self-describing.

HDF4 is an older hierarchical data format as compared to HDF5, which is the latest 
 version promoted by the HDF Group, the publisher of the libraries and standards 
 for these formats. While the transition to HDF5 has occurred for many remote sensing
 products, HDF4 is still the primary data format that is adapted for MODIS data 
 products published by NASA
"""

# Tools to Work With NetCDF Data

"""
Both the HDF4 and HDF5 formats have been adapted by NASA to publish data from Earth 
 Observing System (EOS) missions. These adapted formats, referred to as HDF-EOS, 
 contain additional geolocated data types (point, grid, swath) that can be used 
 to store spatial information that are not supported within the original HDF structure.

HDF4-EOS, the format adapted from HDF4, is the currently used format for MODIS 
 data products. You can review the HDF4-EOS User Guide (section 3.1) to learn more
 about how the HDF4 format has been adapted to support these additional spatial
 data types.

HDF4-EOS files are composed of a directory containing data objects (what we might 
 think of as individual files in a computer directory). Each data object is listed 
 as an individual entry in the directory, which allows the data object to be linked
 with related metadata.

Related data objects can be grouped into datasets consisting of multiple data objects
 (what we might think of subdirectories to organize files within a computer directory).
"""

# Explore HDF4 Files Using HDFView

"""
To familiarize yourself with the HDF4 structure, and explore a particular file’s 
 data objects, you can use the free HDFView tool published by the HDF group.

The sections below walk you through downloading and installing the tool as well 
 as exploring an HF4-EOS file included in the dataset that you downloaded at the 
 top of this page (see: section on What You Need).

Download and Install HDF Viewer:
 In order to download the free HDF viewer from the HDF Group website, you will 
 need to first create a free account.

-You can create a free account by clicking on the “Create Free Account” button 
 on the top-right corner of the download page.
-During the process to create a free account, you will be asked to confirm your 
 email address by entering a code that is emailed to the address that you provided.
-Once you have finished creating an account, you can select the appropriate installer
 for your operating system from the download page.

"""







