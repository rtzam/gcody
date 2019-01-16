from numpy import fromfile, dtype, float32, uint16
from struct import unpack


# reading data from binary formatted stl
# update to get all the information from the file, not just x,y,z
def _from_binary(file, xyz=True):

    # creating data type to read stl
    datatype = dtype([
            (str('normals'), float32, (3, )),
            (str('vectors'), float32, (3, 3)),
            (str('attr'), uint16, (1,))]) # numpy function and data types

    # getting number of triangles
    count_data = file.read(4)

    # calculating count for numpy to known size to read
    count, = unpack(str('<I'), count_data) # struct function

    # checks if the number of triangles is greater than the max
    assert count < 1e8, ('File too large, got {} triangles which \nexceeds the maximum of {}').format(count, 1e8)

    # file is an opened file. This reads the rest of the contents
    data = fromfile(file, dtype=datatype, count=count)

    # parsing through returned data
    x = []
    y = []
    z = []

    # iterating over the elements in data
    for i in data:
        # iterating over the 3 points in every i
        for j in i[1]:
            x.append(j[0])
            y.append(j[1])
            z.append(j[2])

    # closing the file
    file.close()

    return x, y, z

# read an ascii formatted stl file into a list of triangles
# update to get all the information from the file, not just x,y,z
def _from_ascii(file, xyz=True):

    # creating x,y,z values
    x=[]
    y=[]
    z=[]

    # iterating over all lines in file
    for line in file:

        # breaking up lines by spaces
        strarray = line.split()

        # ignoring empty lines
        if len(strarray) == 0:
            continue

        # picks the lines that contain triangle information
        if strarray[0] == 'vertex':

            x.append(float(strarray[1]))
            y.append(float(strarray[2]))
            z.append(float(strarray[3]))


    # closing the file
    file.close()

    return x, y, z


# determines whether the file is in ascii or binary format
# and calls appropriete subfunction
def readstl(file):
    # file is a string to a file

    # trying  to open an ascii file
    try:
        f = open(file, 'r')
        return _from_ascii(f)

    # this type of error means the file is in binary
    # most likely...
    except UnicodeDecodeError:

        # reading as a binary file
        f = open(file, 'rb')

        # gets the first line of the file which is the header
        header = f.read(80)

        # loading data
        return _from_binary(f)

    return




# view a mesh given x,y,z and triangles
def viewmesh(x,y,z, triangles=None, backend='matplotlib',**kwargs):
    '''
    Parameters:

    > X, Y, Z: are arrays of the verticies of a triangle 
    
    '''

    # testing if triangles have been given
    if type(triangles) == type(None):
        # creating list of triangles from the x,y,z points
        triangles = [(i, i+1, i+2) for i in range(0, len(x), 3)]


    # help from
    # http://junweihuang.info/uncategorized/3d-visualization-of-dxf-stl-file-using-mayavi-python-script/
    #plotting the surfaces
    if backend == 'mayavi':

        # mayavi imports
        from mayavi import mlab

        # plotting the stl in mayavi
        mlab.triangular_mesh(x, y, z, triangles, **kwargs)

        # showing the image
        mlab.show()
        return

    # typically slower but more widly used
    elif backend == 'matplotlib':

        # matplotlib imports
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import matplotlib.tri as mtri

        # creating the 3D canvas
        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # triangulting using matplotlib's method
        # this is called inside of plot_trisurf
        # not sure if this saves work by doing it here
        triangles = mtri.Triangulation(x, y, triangles=triangles)

        # plotting the triangles
        ax.plot_trisurf(triangles, z, linewidth=0.2,
                        antialiased=True, **kwargs)

        # showing the image
        plt.show()
        return

    # not sure about keeping this but
    # the graphics are nice!
    elif backend == 'plotly':

        # plotly imports
        import plotly.plotly as py
        import plotly.graph_objs as go

        # getting triangle indicies
        i = [t[0] for t in triangles]
        j = [t[1] for t in triangles]
        k = [t[2] for t in triangles]

        # creating the mesh
        trace = go.Mesh3d(x=x,y=y,z=z,
                          i=i,j=j,k=k,
                          **kwargs)

        # showing image
        py.iplot([trace])
        return

    else:
        # telling user that backend selection was no good
        raise ValueError('Backend: {} not recognized'.format(backend))

    return



# plotting stl file contents as triangle surfaces
def viewstl(file=None, backend='matplotlib', **kwargs):

    # if a file name is passed, this reads the triangles
    if file:
        x, y, z = readstl(file)

    # creating list of triangles from the x,y,z points
    triangles = [(i, i+1, i+2) for i in range(0, len(x), 3)]

    # viewing the mesh
    viewmesh(x,y,z, triangles, backend, **kwargs)

    return
