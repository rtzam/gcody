from numpy import deg2rad, sin,cos, array
from gcody import gcode, gsettings


# start angle for the fractal
global theta

theta = 0

def makeit(g, num=3, order=3,size=500,angle=85,tear_angle=170):

    global theta

    for _ in range(100):
        # making times
        for _ in range(num):
            fractal(g, order, size, angle, tear_angle)

            # gives clockwise motion (turn right)
            theta -= 360/num
        # steping up height
        g.rel_move()
        g.move(z=1, extrude=False)
        g.abs_move()
        g.move(extrude=True)
        

    return

# the recursive method to produce the koch fractal
def fractal(g, order, size, angle, tear_angle):

    global theta

    # base of the recursion
    if order == 0:

        # rotation matrix
        rotation = array([cos(deg2rad(theta)),
                             sin(deg2rad(theta)),
                             0])

        # current position is where it is plus the x and y components of motion 
        pos = g.current_pos + size*rotation

        # appending this position to motion history
        g.move(pos.copy())

    else:

        for i in [angle, 360-tear_angle, angle, 0]:
            
            # recursivly calling fractal
            fractal(g, order-1, size/3, angle, tear_angle)

            # gives counterclockwise motion (turn left)
            theta += i
            
    return

######################################################################

# initalizing gcode object
gset = gsettings(graphics='mayavi')
g = gcode(settings = gset)

g.move(0,0,0, speed=50)

# populating this object with the fractal position
makeit(g)

g.cbar_view()
















