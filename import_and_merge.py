# Name:
# Description: 

# Import system modules
import sys,os

# Import ArcGIS utilities
import arcpy

# Import shutil and zipfile modules
from shutil import rmtree
from zipfile import ZipFile
from glob import glob


# Ask user to input geodatabase file name, the polyline featureclass, and
# the points feature class. Also, ask the user how many observations
# for each subset of the polyline feacture class.

workingFolderPath = ""
outFolderPath = ""

# Input polyline feature class.
defaultParm = "Routes_Pline"
#polylineFC = raw_input('Enter Polyline feature class name prefix [' + defaultParm + ']: ')
polylineFC = raw_input('Enter Polyline feature class name prefix: ')
if not polylineFC:
	polylineFC = defaultParm
intersectFC = "intersect_" + polylineFC

defaultParm = "Routes_Pline.gdb"
#outGeodatabase = raw_input('Enter geodatabase to which the feature classes will be imported [' + defaultParm + ']: ')
outGeodatabase = raw_input('Enter geodatabase to which the feature classes will be imported: ')
if not outGeodatabase:
	outGeodatabase = defaultParm
else:
	# Set the working Geodatabase
	arcpy.env.workspace = workingFolderPath + outGeodatabase
	
# Get a count of the intersect files using glob
numGeoDBs = len(glob(workingFolderPath + polylineFC + "*.gdb.zip"))
 

if not (os.path.isdir(outFolderPath + outGeodatabase)):
	# create output geodatabase if it doesn't exist.
	arcpy.CreateFileGDB_management(outFolderPath, outGeodatabase)

# Initialize the list of feature class names to be merged into 1 feature class.
intersectFCList = []
	
for i in range(1, (numGeoDBs + 1)):
	inGeodatabase =  polylineFC + "_" + str(i) + ".gdb"
	tempIntersectFC = intersectFC + "_" + str(i)
	
	#unzip geodatabase
	inGeodatabaseZipped = inGeodatabase + '.zip'
	if (os.path.isfile(workingFolderPath + inGeodatabaseZipped)):
		print ('unzipping %s', workingFolderPath + inGeodatabaseZipped)
		ZipFile(workingFolderPath + inGeodatabaseZipped).extractall()

	print('Importing from geodatabase, %s' % (workingFolderPath + inGeodatabase))

	# Set the working Geodatabase
	if (os.path.isdir(workingFolderPath + inGeodatabase)):
		arcpy.env.workspace = workingFolderPath + inGeodatabase
	else:
		print('The geodatabase, %s doesn\'t exist. Skipping this database...' % (workingFolderPath + inGeodatabase))
		continue

	# Export feature class: intersectFC
	print('Exporting %s feature classe to geodatabase, %s' % (tempIntersectFC, outFolderPath + outGeodatabase))
	if (arcpy.FeatureClassToGeodatabase_conversion([tempIntersectFC], (outFolderPath + outGeodatabase))):
		# add intersect feature class name to list of intersect names that will be merged.
		intersectFCList.append(tempIntersectFC)
	else:
		print('Exporting feature class, %s was unsuccessful. Hopefully, you never see this message...' % tempIntersectFC)
	
	# Delete extracted geodatabase zipfile.
	rmtree(workingFolderPath + inGeodatabase)
	
# Merge all feature classess we just imported into the outGeodatabase.
arcpy.env.workspace = outFolderPath + outGeodatabase
print('Merging intersect feature classes...')
if (arcpy.Merge_management(intersectFCList, intersectFC + "_merged")):
	print('Merging of intersect feature classes was successful.')
	print('The merged feature class is called: %s.' % (intersectFC + "_merged"))
	# Delete all individual intersect feature classes
	for j in intersectFCList:
		print('Deleting intersect feature class, %s.' % j)
		arcpy.Delete_management(j)
else:
	print('There was a problem merging the intersect feature classes...')

## The End...

	
