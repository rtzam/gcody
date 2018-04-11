# pygcode

Pygcode is a python wrapper for GCODE. It gives common programming language functionality to GCODE as well as some convenient debugging tools. This is a very early draft of pygcode and it is intended for general writing of GCODE, not printer specific code. Pygcode was heavily inspired by [mecode](https://github.com/jminardi/mecode) and has modified some of their code.


### Basics:

[//]: <python code example>
```python
# pyGCODE example creating a serpentine pattern
import pygcode

# creating parameters
distance = 10
cycles = 10

# creating gcode object
g = pygcode.gcode()

# creates a header for the gcode file that implements some basic printer settings
# this step is totally optional
# sets units to mm, sets absolute coordinates, and announces new layer
g.header() 

# moves the print head back and forth in x
# the move command has several options and is the workhourse of the code
g.move(distance, com='Moves head 10 in x') 

# moves the print head back and forth in x
for i in range(1,cycles):
	# simple move allows for modality (not repeating commands)
    # so it has fewer arguments than move
    # it makes the GCODE prettier :)
    g.simple_move(y=10*i) # movement in y
    g.simple_move((-1)**i * distance) # movement in x

# creates a matplotlib figure matching the path of the printer head
g.view('r-o') # passes pyplot.plot arguments as args and kwargs

# saves the GCODE to a file
g.save('snake') # outputs file 'snake.gcode'
g.save('snake','txt') # outputs file 'snake.txt'
```

The output GCODE is:
```GCODE
; This is GCODE generated with pygcode version 0.1.2 
; Written by Ryan Zambrotta 


G21 ; set units to millimeters 
G90 ; use absolute coordinates 
M790  ; announce new layer 


G1 X10.000000 ; Moves head 10 in x 
Y10.000000  
X-10.000000  
Y20.000000  
X10.000000  
Y30.000000  
X-10.000000  
Y40.000000  
X10.000000  
Y50.000000  
X-10.000000  
Y60.000000  
X10.000000  
Y70.000000  
X-10.000000  
Y80.000000  
X10.000000  
Y90.000000  
X-10.000000
```

[//]: <Print head image>
![Printer Path](test_path.png)


### To Do:
* Add clockwise motion commands
* Add more complex combinations of move
* Add in other printer setting commands
* Take requests for features!



















