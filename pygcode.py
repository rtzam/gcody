# second draft of pyGCODE
# version 0.1.2

# imports
from pyvector import *


## Constants ------------------------------------------------------------------------
NAME = 'pygcode' # name of module
VERSION = '0.1.2' # Version of pyGCODE


# helper GCODE class -------------------------------------------------------------


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
        


# class that stores settings for the gcode class
class gcode_settings():

    # init method contains all the default options
    def __init__(self, pos_str='{:0.6f}',speed_str='{}',
                 extrude_str='{:0.6f}'):

        # assigning values to memory
        self.lib = {'pos':pos_str, 'extrude':extrude_str, 'speed':speed_str}
        
        # end of init
        return

    # method to format a string that provides checks on input arguments
    def format(self, lib_arg, x):

        # checks if argument passed is a key in dictionary
        if lib_arg in self.lib:
            return self.lib[lib_arg].format(x)
        else:
            raise ValueError('Key {} not in dictionary'.format(lib_arg))
    
    # methods to use builtin functions ----------------------------------------------
    def __repr__(self):
        return str(self.lib)
    def __str__(self):
        return str(self.lib)
    def __len__(self):
        return len(self.lib)
    def __getitem__(self, lib_arg):
        return self.lib[lib_arg]

        



# Main GCODE class -------------------------------------------------------------

class gcode():

    def __init__(self, debug_mode=False, settings=None):

        # settings
        if not settings:
            # uses default settings
            self.settings = gcode_settings()
            
        elif type(settings) != gecode_settings:
            # type of settings is incorrect
            raise TypeError('Settigns object must be of type gecode_settings')
        else:
            # settings is good to go!
            self.settings = settings

        # creating memory blocks for GCODE
        self.code = []

        # number of lines written
        self.count = 0

        # creating motion history
        self.history = vec2d(shape=(0,3))

        # records the current position
        self.current_pos = [0,0,0]

        # determines whether to only print lines of gcode to screen or to only save to memory
        self.debug = debug_mode

        # recording if a header was used
        self.has_head = False

        # creating a library for user defined commands
        self.user_lib = {}

        # end of init
        return

    

    # writes line of code with command Gl stright line motion
    def move(self, x=None,y=None,z=None,speed=None,extrude=None,com=None):

        # creating line of GCODE
        line = gcode_line('G1', com)

        # checking if given numerical intputs are single values
        if isinstance(x,int) or isinstance(x,float) or isinstance(y,int) or isinstance(y,float) or isinstance(z,int) or isinstance(z,float):
            # appending parameters to line of GCODE
            if x:
                line.append(' X' + self.settings['pos'].format(x) )
                # updating position
                self.current_pos[0] = x
            if y:
                line.append(' Y' + self.settings['pos'].format(y))
                # updating position
                self.current_pos[1] = y
            if z:
                line.append(' Z' + self.settings['pos'].format(z))
                # updating position
                self.current_pos[2] = z
            if speed:
                line.append(' F' + self.settings['speed'].format(mmps2mmpm(speed)))
            if extrude:
                line.append(' E' + self.settings['extrude'].format(extrude))

            # writing to memory
            self.write(line.done(),True)
            # end of move

        else:
            if len(x) == len(y) and len(x) == len(z):
                for i in range(len(x)):
                    # appending parameters to line of GCODE
                    if x[i]:
                        line.append(' X' + self.settings['pos'].format(x[i]) )
                        # updating position
                        self.current_pos[0] = x[i]
                    if y[i]:
                        line.append(' Y' + self.settings['pos'].format(y[i]))
                        # updating position
                        self.current_pos[1] = y[i]
                    if z[i]:
                        line.append(' Z' + self.settings['pos'].format(z[i]))
                        # updating position
                        self.current_pos[2] = z[i]
                    if speed:
                        line.append(' F' + self.settings['speed'].format(mmps2mmpm(v)))
                    if extrude:
                        line.append(' E' + self.settings['extrude'].format(ext))

                    # writing to memory
                    self.write(line.done(),True)  

                return                
                                            
    # end of move

    # allowing for modelity in GCODE same as move but only write x,y,z
    def simple_move(self, x=None,y=None,z=None, write=True,giveit=False):

        # creating line of GCODE
        line = gcode_line()

        # checking if given numerical intputs are single values
        if isinstance(x,int) or isinstance(x,float) or isinstance(y,int) or isinstance(y,float) or isinstance(z,int) or isinstance(z,float):
            # appending parameters to line of GCODE
            if x:
                line.append('X' + self.settings['pos'].format(x) + ' ')
                # updating position
                self.current_pos[0] = x
            if y:
                line.append('Y' + self.settings['pos'].format(y) + ' ')
                # updating position
                self.current_pos[1] = y
            if z:
                line.append('Z' + self.settings['pos'].format(z) + ' ')
                # updating position
                self.current_pos[2] = z

            # writing to memory
            self.write(line.done(),True)

           
            # end of move

        else:
            if len(x) == len(y) and len(x) == len(z):
                for i in range(len(x)):
                    if x[i]:
                        line.append('X' + self.settings['pos'].format(x[i]) + ' ')
                        # updating position
                        self.current_pos[0] = x[i]
                    if y[i]:
                        line.append('Y' + self.settings['pos'].format(y[i]) + ' ')
                        # updating position
                        self.current_pos[1] = y[i]
                    if z[i]:
                        line.append('Z' + self.settings['pos'].format(z[i]) + ' ')
                        # updating position
                        self.current_pos[2] = z[i]

                    # writing to memory
                    self.write(line.done(),True)
                                                    
    # end of simple_move

    

    # takes speed in mmps and writes GCODE in mmpm format
    def speed(self, v=10, com=None):

        # creates GCODE line
        line = gcode_line('F' + self.settings['speed'].format(mmps2mmpm(v)), com)

        # writing to memory
        self.write(line.done())
        return
        # end of speed


    # sets teh units of the system
    def units(self, mm=True):
        
        if mm:
            line = gcode_line('G21', 'set units to millimeters')
            self.unit_sys = 'mm'
        else:
            line = gcode_line('G20', 'set units to inches')
            self.units_sys = 'in'

        # writing to memory
        self.write(line.done())
        return
        # end of units

    
    # sets whether motion is relative to the previous point or on an
    # absolute coordinate system
    def coords(self, absolute=True):

        # determining which coordinate system to use
        if absolute:
            line = gcode_line('G90','use absolute coordinates')
            self.coord_sys = 'abs'
        else:
            line = gcode_line('G91', 'use relative coordinates')
            self.coord_sys = 'rel'

        # writing to memory
        self.write(line.done())
        return
    # end of coords


    # adds a new layer
    def new_layer(self, com='announce new layer'):
        line = gcode_line('M790 ', com)

        # writing to memory
        self.write(line.done())
        return

    # end of new_layer
        
    # writes command to extrude from the printer
    def extrude(self, ext, com=None):
        line = gcode_line('E' + self.settings['extrude'].format(ext), com)

        # writing to memory
        self.write(line.done())
        return
        # end of extrude
        
    # writes command for comments
    def comment(self, com):
        line = gcode_line(comment=com)

        # writing to memory
        self.write(line.done())
        return
        # end of comment

    # command to set home
    def set_home(self,  x=None,y=None,z=None,com='setting home position'):

        # command to set the home position
        line = gecode_line('G28', com)

        if x:
            line.append(' X' + self.settings['pos'].format(x))
        if y:
            line.append(' Y' + self.settings['pos'].format(y))
        if z:
            line.append(' Z' + self.settings['pos'].format(z))

        # recording line to mem
        self.write(line.done())
        # end of set_home
        return

    # method that creates blank lines on the GCODE file
    def blank(self, lines=1):

        # checking the lines
        lines = int(lines)

        # creating black lines
        for i in range(lines):
            # determining how to return values
            self.write(gcode_line().done())

        # end of blank
        return 
    
    # a method that wraps other methods commonly used before any motion
    def header(self):

        # telling object that header has been set
        self.has_head = True

        
        # writing header lines
        self.comment('This is GCODE generated with {} version {}'.format(NAME,VERSION))
        self.comment('Written by Ryan Zambrotta')

        self.blank(2)
        self.units()
        self.coords()
        self.new_layer()
        self.blank(2)

        # end of header
        return
    

    ## IMPORTANT function here. write writes a line to memory as well as parses
    def write(self, line, move=False):

        # increasing counter 
        self.count +=1

        # checking debug mode
        # determining how to return values
        if self.debug:
            print(line)
            return
        else:
            # appending the line of GCODE to the vector of lines
            if move:
                # records motion
                self.history.append(self.current_pos)

            # records GCODE
            self.code.append(line)
            return    

        # end of write 
        return


    

    # Method to visualize the printer path 
    def view(self, *args, backend='matplotlib', fig_title='Print Path',
             give=False,**kwargs):
        
        """ View the path given by the GCODE.

        backend : str (default: 'matplotlib')
            The plotting backend to use, one of 'matplotlib' or 'mayavi'.
            
        *args,**kwargs : are passed to matplotlib's pyplot.plot function
        
        fig_title : the title given to the figure. Only used is a figure is not given to plot on
        
        give : this command makes the method return the figure after the path data is
                plotted. This has no effect when mayavi is the backend.
        """

        # checking backend input and force matplotlib if there is a mistake
        if backend != 'matplotlib' and backend != 'mayavi':

            # create warning message
            warn = 'Incorrect backend ({}) given \nMust be either matplotlib or mayavi \nDefaulting to matplotlib'.format(backend)

            # reassinging backend
            backend = 'matplotlib'

            # raising warning and continuing
            raise Warning(warn)
        
        
        if backend == 'matplotlib':
            from mpl_toolkits.mplot3d import Axes3D
            import matplotlib.pyplot as plt

            # creating figure
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.set_aspect('equal')

            # getting motion history
            X = self.history[:, 0]
            Y = self.history[:, 1]
            Z = self.history[:, 2]

            # To Do add optional label to the first point
            # Plots the 3 past printer positions on figure
            ax.plot(X, Y, Z, *args, **kwargs)

            # Keeps aspect ratio square
            # http://stackoverflow.com/questions/13685386
            max_range = np.array([X.max()-X.min(),
                                  Y.max()-Y.min(),
                                  Z.max()-Z.min()]).max() / 2.0

            mean_x = X.mean()
            mean_y = Y.mean()
            mean_z = Z.mean()
            ax.set_xlim(mean_x - max_range, mean_x + max_range)
            ax.set_ylim(mean_y - max_range, mean_y + max_range)
            ax.set_zlim(mean_z - max_range, mean_z + max_range)

            # labeling figure axes and title
            ax.set_xlabel('X ({})'.format(self.unit_sys))
            ax.set_ylabel('Y ({})'.format(self.unit_sys))
            ax.set_zlabel('Z ({})'.format(self.unit_sys))
            plt.title(fig_title)


            # determines whether to show the figure or to return it
            if give:
                return ax
            else:
                # showing figure
                plt.show()

            # end of view
            return

        # mayavi 
        elif backend == 'mayavi':
            from mayavi import mlab

            # plotting the time series
            mlab.plot3d(self.history[:, 0],
                        self.history[:, 1],
                        self.history[:, 2],
                        *args, **kwargs)

            # labeling axes and title
            mlab.xlabel('X ({})'.format(self.unit_sys))
            mlab.ylabel('Y ({})'.format(self.unit_sys))
            mlab.zlabel('Z ({})'.format(self.unit_sys))
            mlab.title(title)

            # end of view
            return

    
    # writes the output to a file
    def save(self, file, ext='gcode'):

        #  save file name
        save_file = file + '.' + ext

        # opening and creating file
        with open(save_file,'w') as f:
            # iterating over all elements in sel.code
            for i in range(len(self.code)):
                # writing to file
                f.write(self.code[i])

            # closing text file
            f.close()

        # end of store
        return

    # creates the string and print representation of the gcode    
    def give(self, store=False, update=True):

        if update:
            # creates variable to store all of code
            print_item = ''

            # if no lines are written then empty list is returned
            if len(self.code) == 0:
                return '[]'
            else:
                # iterative over all lines of gcode and append to print_item
                for i in range(len(self.code)):
                    print_item += self.code[i]

        else:
            # recursively defines self.print_item
            if not self.print_item:
                self.give(True,True)
        
        if store:
            # stores the returned item
            self.print_item = print_item
        
        return print_item


    # functions that give the printing options of the GCODE 
    def __repr__(self):
        # creates a print object and returns that 
        return self.give()
        
    def __str__(self):
        # creates a print object and returns that
        return self.give()

    # gives [] indexing access to the gcode vector
    def __getitem__(self, index):
        return self.code[index]

    # gives built in len function access to self.code
    def __len__(self):
        return len(self.code)




## Helper functions ------------------------------------------------------------------

# converts milimeters per second in GCODE standard milimeters per minute
def mmps2mmpm(v=1):
    return v*60
# converting milimeters per minute in GCODE standard milimeters per second
def mmpm2mmps(v=1):
    return v/60



























        
