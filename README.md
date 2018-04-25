# pygcode

Pygcode is a python wrapper for GCODE. It gives common programming language functionality to GCODE as well as some convenient debugging tools. 
This is a very early draft of pygcode and it is intended for general writing of GCODE, not printer specific code. 
Pygcode was heavily inspired by [mecode](https://github.com/jminardi/mecode).


### Basics:

<python code example>

```python
# pyGCODE example creating a serpentine pattern
from pygcode import gcode

# creating parameters
distance = 10
cycles = 10

# creating gcode object
g = gcode()

# writes the GCODE command to use relative coordinates
# this changes how position is recorded internally and will be displayed differently
# when g.view is called below()
# abs_coords is the default setting for gcode and is the default for pygcode as well
g.rel_coords()


# setting the speed for the print head
# input is in per second units and is converted to per minute
g.speed(10, '10 mmps motion') 

# moves the print head back and forth in x
g.move(distance, com='Moves head 10 in x')


# moves the print head back and forth in x
for i in range(1,cycles):
    # simple move allows for modality (not repeating commands)
    # it makes the GCODE prettier :)
    # unfortunately not all printers support it :(
    g.simple_move(y=10) # movement in y
    g.simple_move((-1)**i * distance) # movement in x

# creates a matplotlib figure matching the path of the printer head
# defaults to a 4D plot with time represented as color
g.view() # passes pyplot.plot argument as args and kwargs

# saves the GCODE to a file
g.save('snake') # outputs file 'snake.gcode'
g.save('snake','txt') # outputs file 'snake.txt'
```

The output GCODE is:
```GCODE
G91 ; use relative coordinates 
F600 ; 10 mmps motion 
G1 X10.000000 ; Moves head 10 in x 
Y10.000000  
X-10.000000  
Y10.000000  
X10.000000  
Y10.000000  
X-10.000000  
Y10.000000  
X10.000000  
Y10.000000  
X-10.000000  
Y10.000000  
X10.000000  
Y10.000000  
X-10.000000  
Y10.000000  
X10.000000  
Y10.000000  
X-10.000000  
```

<Print head image>

![Printer Path](test_path.png)


### Dependancies:
* [pyvector](https://github.com/rtZamb/pyvector) which requires numpy



### To Do:
* Add clockwise motion commands
* Add more complex combinations of move
* Add in other printer setting commands
* Take requests for features!



















