""""------------------------------------------------------------------------------
Name:         		split.py
			  
Description:    	This script splits a polyline feature class of large volume into multiple feature
classes of polylines of small volume, which are then stored in separate geodatabases with the point
feature class. Finally it zips all those geodatabases and deletes the unzipped geodatabases.
-------------------------------------------------------------------------------"""
# Import os and sys python modules which allow python to use file based functions
# and utilities.
import os, shutil

# Import ArcGIS modules
import arcpy 

print "Splitting..."

# Input the geodatabase file name, the polyline featureclass, and
# the points feature class. Also, ask the user how many observations
# for each subset of the polyline feacture class.
arcpy.env.workspace = "Routes4_Pline.gdb"
# Input polyline feature class.
routesFC = "Routes4_Pline"
pointsFC = "Station_Points"

# Get the total number of entries in poly-line feature class.
numObservations = int(arcpy.GetCount_management(routesFC).getOutput(0))

# Input the size of each subset class
subsetEntries = 10000

###############################################################################
# Create subset feature classes 
# No. of feature classes after spliting (i.e. integer)
# The '//' divides the numbers and returns a number without the remainder.
numNewFeatureClasses = (numObservations // subsetEntries) + 1   

print("Splitting data into %i parts" % numNewFeatureClasses)

# start loop to create subsets...
for i in range(1, (numNewFeatureClasses + 1)):

	# Set up the SQL Where clause that will be used to select certain rows of the large feature class.
	subsetFC = routesFC + '_' + str(i)
	outGeodatabase = subsetFC + '.gdb'
	
	startNdx = ((i-1) * subsetEntries) + 1
	endNdx = startNdx + subsetEntries - 1
	whereClause = '"OBJECTID_1" >= ' + str(startNdx) + ' AND "OBJECTID_1" <= ' + str(endNdx)

	# Create new feature class from range of rows.
	arcpy.Select_analysis(routesFC, subsetFC, whereClause)

	# Create Geodatabase
	arcpy.CreateFileGDB_management(".", outGeodatabase)

	# Export newly created feature class and feature class: Station_Points
	arcpy.FeatureClassToGeodatabase_conversion([subsetFC, pointsFC], outGeodatabase)

	# Delete newly created subset feature class from inGeodatabase		
	arcpy.Delete_management(subsetFC)
	
	# Zip up newly created geodatabase
	print('Zipping %s out of %s' % (i, numNewFeatureClasses))
	shutil.make_archive(outGeodatabase, 'zip', ".", outGeodatabase) #Archiving zipped geodatabases
	
        # Delete unzipped geodatabase from temporary output folder
	shutil.rmtree(outGeodatabase)

print "Complete!"
