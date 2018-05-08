# gcody example creating a serpentine pattern and an elephant

# these are both normally imported from gcody
from gcode import gcode
from readg import read

# creating parameters
distance = 10
cycles = 10

# creating gcode object
g = gcode()

# writes the GCODE command to use relative coordinates
# this changes how position is recorded internally and will be displayed differently
# when g.view is called  below()
# abs_coords is the default setting for gcode and is the default for pygcode as well
g.rel_move()

# moves the print head back and forth in x
g.move(distance, speed=10, com='Moves head 10 in x')


# moves the print head back and forth in x
for i in range(1,cycles):
    # simple move allows for modality (not repeating commands)
    # it makes the GCODE prettier :)
    # unfortunately not all printers support it :(
    g.simple_move(y=10) # movement in y
    g.simple_move((-1)**i * distance) # movement in x

# creates a matplotlib figure matching the path of the printer head
g.view('b')

# This is an animated figure showsing the progression of the printer path
g.animated('b',save_file='snake.gif')


# saves the GCODE to a file
g.save('snake') # outputs file 'snake.gcode'
g.save('snake','txt') # outputs file 'snake.txt'


########################################################################################
# demo of reading GCODE

# file from https://www.thingiverse.com/thing:998999/#files
file = 'elefante_small.gcode'

# This Reads the GCODE file line by line and converts it into a gcode object
# preallocating with the number of lines in the file for speed
# GCODE file can be hundreds of thousands of lines, if not more. This means reading them
# can be very slow.
elefante = read(file, n_lines=16005)

# This figure colors the lines draw with a color that corresponds to a print time
elefante.cbar_view() # rendering all the colors can a while

# this view has a slider bar that allows one to select the print time
elefante.slide_view('r')




















