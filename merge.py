# Import system modules
import sys, os, shutil, glob
from zipfile import ZipFile

# Import ArcGIS utilities
import arcpy

# Input polyline feature class.
routesFC = "Routes4_Pline"

intersectFC = "intersect_" + routesFC

# Initialize the list of feature class names to be merged into 1 feature class.
intersectFCList = []

# Define the Geodatabase
mainGeodatabase = "Routes4_Pline.gdb"

# Get a count of the intersect files using glob
geoDBList = glob.glob("*.gdb.zip")
numGeoDBs = len(geoDBList)

for i in range(1, numGeoDBs + 1):
    inGeodatabase = routesFC + "_" + str(i) + ".gdb"
    currIntersectFC = intersectFC + "_" + str(i)

    # Unzip geodatabase
    inGeodatabaseZipped = inGeodatabase + ".zip"
    ZipFile(inGeodatabaseZipped).extractall()

    # Set the working Geodatabase
    arcpy.env.workspace = inGeodatabase

    # Export feature class: intersectFC
    arcpy.FeatureClassToGeodatabase_conversion([currIntersectFC], mainGeodatabase)
    intersectFCList.append(currIntersectFC)
    print "Adding file %s out of %s" % (i, numGeoDBs)

    # Delete extracted geodatabase zipfile.
    shutil.rmtree(inGeodatabase)
    os.remove(inGeodatabase + ".zip")

# Set the working Geodatabase to original    
arcpy.env.workspace = mainGeodatabase

# Merge all feature classess we just imported into the outGeodatabase.
print "Merging..."
arcpy.Merge_management(intersectFCList, intersectFC + "_merged")

# Delete all individual intersect feature classes
for listToDel in intersectFCList:
    arcpy.Delete_management(listToDel)
print "Complete!"
