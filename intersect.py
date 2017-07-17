import os, sys, shutil
from zipfile import ZipFile
import arcpy

# Set parameters to be used in the intersect analysis function
routesFC = sys.argv[1]
stationsFC = sys.argv[2]
intersectFC = "intersect_" + routesFC
workingGDB = routesFC + ".gdb"

# Extract zipped files
ZipFile(workingGDB + ".zip").extractall()

# Set the working Geodatabase
arcpy.env.workspace = workingGDB

# Run the intersect analysis function
arcpy.Intersect_analysis([routesFC, stationsFC], intersectFC)

# Zip up the geodatabase
shutil.make_archive(workingGDB, 'zip', ".", workingGDB)

# Remove unzipped files
shutil.rmtree(workingGDB)
