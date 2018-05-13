# gcody example creating a serpentine pattern and an elephant

# these are both normally imported from gcody
from gcody import gcode, read

# creating parameters
distance = 10
cycles = 10

# creating gcode object
g = gcode()

# writes the GCODE command to use relative coordinates
# this changes how position is recorded internally (in gcode object)
# abs_coords is the default setting for gcode and is the default for gcody as well
g.rel_move()

# This command moves the printer 10 mm foward in the x
# at a speed of 10 mmps
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
g.animated('b', save_file='snake.gif')


# saves the GCODE to a file
g.save('snake') # outputs file 'snake.gcode'
g.save('snake','txt') # outputs file 'snake.txt'


########################################################################################
# demo of reading GCODE

# file from https://www.thingiverse.com/thing:998999/#files
file = 'elefante_small.gcode'

# This reads the GCODE file line by line and converts it into a gcode object
# GCODE file can be hundreds of thousands of lines, if not more. This means reading them
# can be slow. The math comes out to is roughly 13,000 move lines per second.
elefante = read(file)

# This figure colors the lines draw with a color that corresponds to a print time
elefante.cbar_view() # rendering all the colors can a while

# this view has a slider bar that allows one to select the print time
elefante.slide_view('r')


