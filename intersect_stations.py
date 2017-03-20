# Name:
# Description: 

# Import system modules
import os,sys
import arcpy

from shutil import make_archive,rmtree
from zipfile import ZipFile
from glob import glob

print('argv[1] = %s' % sys.argv[1])
print('argv[2] = %s' % sys.argv[2])

for z in glob('*.zip'):
	print ('for z in glob: %s', z)
	ZipFile(z).extractall()

# Set the working Geodatabase
arcpy.env.workspace = sys.argv[1] + ".gdb"

# Set parameters to be used in the intersect analysis function
routeFeatureClass = sys.argv[1]
print ('routeFeatureClass = %s', routeFeatureClass)
stationsFeatureClass = sys.argv[2]
print ('stationsFeatureClass = %s', stationsFeatureClass)
outIntersectFeatureClass = "intersect_" + sys.argv[1]
print ('outIntersectFeatureClass = %s', outIntersectFeatureClass)

# Run the intersect analysis function
arcpy.Intersect_analysis([routeFeatureClass, stationsFeatureClass], outIntersectFeatureClass)

# Zip up the geodatabase
for z in glob((sys.argv[1] + ".gdb")):
  print ('zipping %s...' % z)
  make_archive('%s' % z, 'zip', os.getcwd(), z)
  print ('done zipping %s' % z)
  
# Delete the overlay.txt file
for f in glob('Overlay.txt'):
  os.unlink(f)

for e in glob('*.gdb'):
  rmtree(e)