
# getting imports
from gcody import gcode, read
from stlview import viewmesh
from scipy.spatial import Delaunay
from numpy import array


def surfg_np(file, **kwargs):

    # reading the gcode file
    gcode_obj = read(file)

    # converting to a numpy array
    data = array(gcode_obj.history)

    # running Delaunary algorithm for triangulation
    tri = Delaunay(data[:,0:2])

    # viewing the generated mesh
    viewmesh(data[:,0], data[:,1], data[:,2],
             tri.simplices, backend='mayavi', **kwargs)

    return


# plotting the surface from gcode
def surfg(file, **kwargs):

    # reading the gcode file
    gcode_obj = read(file)
    
    #getting points from gcode_object
    points = [[i[0], i[1]] for i in gcode_obj.history]
    x = [i[0] for i in gcode_obj.history]
    y = [i[1] for i in gcode_obj.history]
    z = [i[2] for i in gcode_obj.history]

    # running Delaunary algorithm for triangulation
    tri = Delaunay(points)

    # viewing the generated mesh
    viewmesh(x, y, z, tri.simplices, backend='mayavi', **kwargs)

    return



############################################################################
##########################################################################
# testing

# input file
file = 'elefante_small.gcode'

# viewing the gcode
surfg(file)




















