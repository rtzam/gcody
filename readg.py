'''
Module that contains a class to parse through GCODE and recreate what the
code does!

Written by Ryan Zambrotta
'''
from gcode import gcode


# Contains a function to read GCODE from a file and create a gcode object that contains
# the same information
def read(file):

    # list that will hold all the lines in the file given
    lines = []

    # open give file as read only
    with open(file, 'r') as f:

        # iterating over all lines in file f
        for line in f:

            # appending all to lines
            lines.append(line)

        # closing file
        f.close()

    # create a gcode object that will be returned after all the lines of GCODE are parsed
    # through
    temp = gcode()

    # iterating over all lines and parsing out the commands from the GCODE
    for i in lines:

        # removes whitespace from the beginning and end of the string
        line = i.lstrip()
        line = line.rstrip()

        # breaks up the line into components seperated by space
        commands = line.split(' ')
































        
        
        
    
    
