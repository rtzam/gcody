## 3rd draft of pyGCODE
# version 0.1.3

# imports
from vector import *

## constants ---------------------------------------------------------------------
NAME = 'pyGCODE' # name of module
VERSION = '0.1.3' # Version of pyGCODE

## helper classes ------------------------------------------------------------------


# base class that represents a single line of gcode
class gcode_line():

    def __init__(self, command=None, comment=None):

        # creates the gcode command
        if command:
            self.line = command
        else:
            # if no command is given then an empty line
            self.line = ''


        # stores the comment
        self.comment = comment

        # end of init
        return

    # methods ----------------------------------------------------------------------

    # method to append items to line
    def append(self, text):
        self.line += str(text)


    # method that adds the comment to the line once all text has been added
    def done(self):

        # adds comment to line
        if self.comment:
            # adds the comment with the gcode comment command
            if self.line == '':
                # if no command is given, comment format is different
                self.line += '; ' + self.comment + ' \n'
            else:
                # standard comment added to line of gcode
                self.line += ' ; ' + self.comment + ' \n'
        else:
            if self.line == '':
                self.line = '\n'
            else:
                # if no comment is given then a new line is created
                self.line += ' \n'
        
        # just returns line
        return self.line   
        
    # ---------------------------------------------------------------------------------
    # methods for builtin function access
    
    # creates functions that determing printing behavior
    def __repr__(self):
        return self.line
    def __str__(self):
        return self.line

    # gives the length of the line
    def __len__(self):
        return len(self.line)




# Class that represents a single GCODE command
class gcode_lib():

    def __init__(self, **kwargs):

        # records the builtin GCODE functions
        # what command does and GCODE command
        self.commands = {'move':'G1','speed':'F','mm':'G21','in':'G20',
                    'abs coords':'G90','rel coords':'G91','new layer':'M790',
                    'extrude':'E','comment':';','set home':'G28','rapid move':'G0',
                    'clockwise move':'G2','counterclockwise move':'G3'}

        # creats a user defined dictionary of gcode commands
        self.user_commands = dict(**kwargs)

        # joins two dictionaries
        self.lib = self.commands.update(self.user_commands)



        
        return
    # end of init


def test():
    return 'yay!'




































