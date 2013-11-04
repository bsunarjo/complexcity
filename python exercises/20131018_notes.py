# import the proper files
from shapely.geometry import *
import blender_show as show

# create a 2d or 3d point
p = Point(1,2,3)

# Buffer: offset from a geometric shape
a = Point(1,1).buffer(1.5)
b = Point(1,2).buffer(1.5)


# Reload scripts
import imp
imp.reload(show)


# Access to blender internals
# for all manner of interaction
import bpy
bpy.data # Blender file -> outline, datablockss