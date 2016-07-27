#!/usr/bin/env python

""""------------------------------------------------------------------------------
name:         split_feature_class.py
arguments:    
			  
version:      python 2.7

dependencies: 
			  
description:    
-------------------------------------------------------------------------------"""
# Import os and sys python modules which allow python to use file based functions
# and utilities.
import os,sys

# Import ArcGIS modules
import arcpy

from shutil import rmtree,make_archive
from zipfile import ZipFile
from glob import glob

# Setup file names and feature class names.
inGeoDatabase = "Routes4_Pline.gdb"
largePolyLineFCName = "Routes4_Pline"
pointsFCName = "Station_Points"

workingFolderPath = "C:\\ClemsonGISGitHub\\ArcGISVectorIntersects\\"
outFolderPath = "C:\\GISSplitVector\\"

# Set the working Geodatabase
arcpy.env.workspace = workingFolderPath + inGeoDatabase

# Get total number of entries in poly-line feature class.
result = arcpy.GetCount_management(largePolyLineFCName)
numObservations = int(result.getOutput(0))


###############################################################################
# Create subset feature classes 



# Get a count of the observations
numberObservationsPerFeatureClass = 5000   # Make this command line argument later?

print('total count of feature class, %s = %i' % (largePolyLineFCName, numObservations))


# Set the working Geodatabase
#arcpy.env.workspace = (outFolderPath + outGeoDBName)
numNewFeatureClasses = (numObservations // numberObservationsPerFeatureClass) + 1
#tallyNumOfFeatureClasses += numNewFeatureClasses
print ("numNewFeatureClasses for feature class, %s = %i" % (largePolyLineFCName, numNewFeatureClasses))
for i in range(1, (numNewFeatureClasses + 1)):
	# Set up the SQL Where clause that will be used to select certain rows of the large feature class.
	outFeatureClass = largePolyLineFCName + '_' + str(i)
	print ('outFeatureClass = %s' % outFeatureClass)
	obsIdx = (i-1) * numberObservationsPerFeatureClass
	whereClause = '"OBJECTID_1" > ' + str(obsIdx) + ' AND "OBJECTID_1" <= ' + str((obsIdx + numberObservationsPerFeatureClass))
	print ('whereClause = %s' % whereClause)

	# Create new feature class from range of rows.
	print ('Creating subset feature class...')
	arcpy.Select_analysis(largePolyLineFCName, outFeatureClass, whereClause)

	# Create Geodatabase
	outGeoDBName = outFeatureClass + '.gdb'
	print ('Creating new geodatabase, %s' % outGeoDBName)
	arcpy.CreateFileGDB_management(outFolderPath, outGeoDBName)

	# Export newly created feature class and feature class: Station_Points
	print ('Exporting feature classes, %s and %s' % (outFeatureClass, pointsFCName))
	arcpy.FeatureClassToGeodatabase_conversion([outFeatureClass, pointsFCName], (outFolderPath + outGeoDBName))
	
	# Zip up newly creatd geodatabase and delete gdb folder.
	z = outGeoDBName
	print ('zipping %s...' % z)
	make_archive('%s' % z, 'zip', outFolderPath, z)
	print ('done zipping %s' % z)
	
	# Delete unzipped geodatabase
	rmtree(outFolderPath + z)
	




