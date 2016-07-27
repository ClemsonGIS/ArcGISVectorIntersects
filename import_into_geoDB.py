# Name:
# Description: 



# Import system modules
import sys,os

# Import ArcGIS utilities
import arcpy


largePolyLineFCName = "intersectedPlineRoutes"
pointsFCName = "Station_Points"

numGeoDBs = int(sys.argv[1])
	

outFolderPath = "C:\\GISSplitVector\\intersect\\" 
geoDBName = "intersectedPlineRoutes.gdb"


for i in range(1, (numGeoDBs + 1)):
	routesFeatureClass = "Routes" + str(routesNum) + "_Pline_" + str(i)
	intersectFeatureClass = "intersectRoutes" + str(routesNum) + "_Pline_" + str(i)
	inGeoDBName = routesFeatureClass + ".gdb"
	print('Importing from geodatabase, %s' % inGeoDBName)
	
	# Set the working Geodatabase
	arcpy.env.workspace = outFolderPath + inGeoDBName

	# Export newly created feature class and feature class: Station_Points
	print('Exporting %s and %s feature classes to geodatabase, %s' % (routesFeatureClass, intersectFeatureClass, geoDBName))
	arcpy.FeatureClassToGeodatabase_conversion([routesFeatureClass, intersectFeatureClass], (outFolderPath + geoDBName))


	
