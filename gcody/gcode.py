'''
Class gcode written by Ryan Zambrotta
'''

# imports -----------------------------------------------------------------------
from .gline import gline
from .gsettings import gsettings
from .helper import *
from .visual import *
from numpy import array, zeros, any, all, shape
from numpy.linalg import norm


# Main GCODE class -------------------------------------------------------------

class gcode():

    def __init__(self, debug_mode=False, settings=None):
        '''
        Parameters:

        > DEBUG_MOVE: This causes nothing to be saved internally. It is automatically
        > SETTINGS: This is a gsettings object that that contains a dictionary
            of strings to format numbers for specific gcode commands
        '''

        # settings
        if not settings:
            # uses default settings
            self.settings = gsettings()

        elif type(settings) != gsettings:
            # type of settings is incorrect
            raise TypeError('Settigns object must be of type gecode_settings')
        else:
            # settings is good to go!
            self.settings = settings

        # creating memory blocks for GCODE
        self.code = []

        # number of lines written
        self.count = 0

        # creating motion history list
        self.history = []

        # records the current and previous position
        self.current_pos = zeros(3) # numpy
        self.previous_pos = zeros(3) # numpy

        # determines whether to only print lines of gcode to screen or to only save to memory
        self.debug = debug_mode

        # sets the default motion type for move (absolute coordinates)
        self.coords = 'abs'

        # sets default for
        self.unit_sys = 'mm'

        # internal recording of the total print time
        self.print_time = 0 # units of minutes

        # internal recording of time at each motion
        self.t = []

        # recording the print speed
        self.print_speed = 0

        # Contains names of all the method in GCODE
        self.gcode_methods = {'G0':self.rapid_move,'G1':self.move,'G4':self.dwell,
                              'G10':self.retract,'G11':self.unretract,
                              'G20':self.use_in,'G21':self.use_mm,'G28':self.go_home,
                              'G90':self.abs_move,'G91':self.rel_move,'G92':self.set_pos,
                              'M30':self.manual_mask_off,
                              'M82':self.rel_extrude,'M83':self.abs_extrude,'M84':self.stop_idle,
                              'M103':self.stop_extrude,'M104':self.extruders_off,
                              'M106':self.fan,
                              'M107':self.fan_off,'M190':self.wait_for_temp,'M721':self.unprime,
                              'M734':self.err_report,
                              'M756':self.first_layer_thick,'M790':self.new_layer,
                              ';':self.comment,'\n':self.blank}

        # end of init
        return



    ######################################################################################
    ## GCODE Commands--------------------------------------------------------------------
    ## ------------------------------------------------------------------------------------
    ######################################################################################



    # writes line of code with command Gl stright line motion
    def move(self, x=None,y=None,z=None,speed=None,extrude=None,check_end=None,com=None):
        '''
        Parameters:

        > X: The x coordinate to move the print head to. X can be an int,float, or array
            of shape (n,) or (n,3). If shape is (n,), then each element is used
            sequentially as the x coordinate for each motion (each element in the array).
            If X has shape (n,3), then each column is defined as x,y,z and each row is a
            subsequent movement.
        > Y: the y coordinate to move the print head to. Behaves the same as X except for
            that only arrays of shape (n,) can be passed.
        > Z: the z coordinate to move the print head to. Behaves the same as X except for
            that only arrays of shape (n,) can be passed.
        > SPEED: The speed to move the print head for this motion. This input should
            be in the same units as the attribute UNIT_SYS
        > EXTRUDE: The volume to extrude for this motion.... NEED MORE HERE
        > CHECK_END: determines whether the printer checks if an endstop was hit. Default
            to '0'. Options are '0', '1','2'. '1' makes printer check. '2' is more
        > COM: The comment to be added at the end of the lines
        '''

        # checking if x input is a a single value, or an array

        # ensuring that x exists before splitting up x
        if any(x) or any(x == 0):

            temp_shape = shape(x) # numpy
            if len(temp_shape) == 2:

                # (n,3) array x is broken into x,y,z components
                if temp_shape[1] == 3:
                    y = x[:,1]
                    z = x[:,2]
                    x = x[:,0]
                else:
                    raise ValueError('The input array must have shape (n,3) or (n,) but has shape {}'.format(temp_shape))


            # making a list-like object with shape (3,) into x,y,z
            elif len(temp_shape) == 1:

                # (n,3) array x is broken into x,y,z components
                if temp_shape == (3,):
                    y = x[1]
                    z = x[2]
                    x = x[0]
                else:
                    raise ValueError('The input array must have shape (n,3) or (n,) but has shape {}'.format(temp_shape))






        # create a temperary variable to store position to eventually pass to
        # hidden methods to internally record motion
        if self.coords == 'abs':
            pos = self.current_pos.copy()
        else:
            pos = zeros(3) # numpy

        # checking if given numerical intputs are single values
        if isinstance(x,(int,float)) or isinstance(y,(int,float)) or isinstance(z,(int,float)):

            # creating line of GCODE
            line = gline('G1', com)

            # calling hidden function to do the string formatting
            # This command writes the gcode line to memory
            self._move_format(line,pos,
                              x,y,z,
                              speed,extrude)



        # if no positional commands are give and only speed, extrude, and comment are needed
        elif x == None and y == None and z == None:

            # Creating line of gcode
            line = gline('G1', com)

            # writing only speed and extrude
            self._move_format(line, speed=speed, extrude=extrude)

        else:
            # array case
            if len(x) == len(y) and len(x) == len(z):

                # Creating GCODE line for all row in x
                for i in range(len(x)):

                    # creating line of GCODE
                    line = gline('G1', com)

                    # calling hidden function to do the string formatting
                    # This command writes the gcode line to memory
                    self._move_format(line,pos,x[i],y[i],z[i],speed,extrude)

                return
    # end of move



    # allowing for modelity in GCODE same as move but only write x,y,z
    def simple_move(self, x=None,y=None,z=None):
        '''
        Parameters:

        See Move for X,Y,Z

        '''

        # ensuring that x exists before splitting up x
        if any(x) or any(x == 0):

            temp_shape = shape(x) # numpy
            if len(temp_shape) == 2:

                # (n,3) array x is broken into x,y,z components
                if temp_shape[1] == 3:
                    y = x[:,1]
                    z = x[:,2]
                    x = x[:,0]
                else:
                    raise ValueError('The input array must have shape (n,3) or (n,) but has shape {}'.format(temp_shape))


            # making a list-like object with shape (3,) into x,y,z
            elif len(temp_shape) == 1:

                # (n,3) array x is broken into x,y,z components
                if temp_shape == (3,):
                    y = x[1]
                    z = x[2]
                    x = x[0]
                else:
                    raise ValueError('The input array must have shape (n,3) or (n,) but has shape {}'.format(temp_shape))


        # create a temperary variable to store position to eventually pass to
        # hidden methods to internally record motion
        if self.coords == 'abs':
            pos = self.current_pos.copy()
        else:
            pos = zeros(3) # numpy

        # checking if given numerical intputs are single values
        if isinstance(x,(int,float)) or isinstance(y,(int,float)) or isinstance(z,(int,float)):

            # creating an empty line of GCODE
            line = gline()

            # calling hidden function to do the string formatting
            # this writes this to memory
            self._move_format(line,pos,x,y,z)

            # end of move

        else:

            # array case
            if len(x) == len(y) and len(x) == len(z):

                # Creating GCODE line for all row in x
                for i in range(len(x)):

                    # creating line of GCODE
                    line = gline()

                    # calling hidden function to do the string formatting
                    self._move_format(line,pos,x[i],y[i],z[i])


    # end of simple_move


    # method that tells the print to move to X,Y,Z at the max speed
    def rapid_move(self, x=None,y=None,z=None,speed=None,extrude=None,com=None):
        '''
        Parameters:

        See move
        '''

        # ensuring that x exists before splitting up x
        if any(x) or any(x == 0):

            temp_shape = shape(x) # numpy
            if len(temp_shape) == 2:

                # (n,3) array x is broken into x,y,z components
                if temp_shape[1] == 3:
                    y = x[:,1]
                    z = x[:,2]
                    x = x[:,0]
                else:
                    raise ValueError('The input array must have shape (n,3) or (n,) but has shape {}'.format(temp_shape))


            # making a list-like object with shape (3,) into x,y,z
            elif len(temp_shape) == 1:

                # (n,3) array x is broken into x,y,z components
                if temp_shape == (3,):
                    y = x[1]
                    z = x[2]
                    x = x[0]
                else:
                    raise ValueError('The input array must have shape (n,3) or (n,) but has shape {}'.format(temp_shape))


        # create a temperary variable to store position to eventually pass to
        # hidden methods to internally record motion
        if self.coords == 'abs':
            pos = self.current_pos.copy()
        # This if statement is needed to adjust internal recording of position given rel
        # vs. abs coord system
        else:
            pos = zeros(3) # numpy

        # checking if given numerical intputs are single values
        if isinstance(x,(int,float)) or isinstance(y,(int,float)) or isinstance(z,(int,float)):

            # creating line of GCODE
            line = gline('G1', com)

            # calling hidden function to do the string formatting
            # which also writes to memory
            self._move_format(line,pos,x,y,z,speed,extrude)

            # end of move

        else:
            # array case,
            if len(x) == len(y) and len(x) == len(z):

                # Creating GCODE line for all row in x
                for i in range(len(x)):

                    # creating line of GCODE
                    line = gline('G1', com)

                    # calling hidden function to do the string formatting
                    self._move_format(line,pos,
                                      x[i],y[i],z[i],
                                      speed,extrude)
            else:
                raise ValueError('Input arrays must be of same length')

                return

    # end of move


    # method that tells printer to dwell for a specified amount of time
    # this adds s line to motion history and time. This is the current position
    # but the time vector stores the given time at this location
    def dwell(self, sec=None, milisec=None, com=None):
        '''
        Parameters:

        > SEC: the time to wait in seconds
        > MILISEC: the time to wait in miliseconds

        * Notes: SEC takes is defaulted to if both are given. Please only use
            one though!
        '''

        # creating GCODE command
        line = gline('G4',com)

        # adding the time to wait
        if sec:
            # generating the length of time
            line.append('S{}'.format(sec))

            # writing to memory with time in units of minutes
            self.write(line, self.current_pos, time/60)
            return

        elif milisec:
            # generating length of time
            line.append('P{}'.format(milisec))

            # writing to memory with time in units of minutes
            self.write(line, self.current_pos, time/(60*1000))

            return
        else:
            raise RuntimeError('No time given to dwell')

    # method tells printer to retract the print head
    def retract(self, short=None, com='Retracting Head'):
        '''
        Parameters:

        > SHORT:
        '''

        # writing GCODE line
        line = gline('G10', com)

        # Adding the parameter to the retract statement
        if short == 0:
            line.append('S0')
        elif short == 1:
            line.append('S1')


        # technically this moves the head so i need to reserach this more
        self.write(line)
        return

    def unretract(self, short=None, com='Unretracting Head'):
        '''
        Parameters:

        > SHORT:
        '''

        # writing GCODE line
        line = gline('G11', com)

        # Adding the parameter to the retract statement
        if short == 0:
            line.append('S0')
        elif short == 1:
            line.append('S1')


        # technically this moves the head so i need to reserach this more
        self.write(line)
        return



    def use_mm(self, com='set units to millimeters'):

        # create the gcode line and the comment
        line = gline('G21', com)

        # internally recording the distance units
        self.unit_sys = 'mm'

        # writing the line to memory
        self.write(line)
        return

    def use_in(self, com='set units to inches'):

        # creates the line of gcode with inches command and comment
        line = gline('G20', com)

        # internally recording unit system
        self.unit_sys = 'in'

        # writing to memory
        self.write(line)
        return

    # command that moves specific printer axes to their home position
    def go_home(self, safe=False, x=None,y=None,z=None,com='Going to home position'):
        '''
        Parameters:

        > X,Y,Z:
        > COM: the comment on the line
        > SAFE: Default is true. This uses a relatively safer way of moving
            home by raising the Z axis first to avoid hitting anything,
            then returning home. CAUTION: This switches to relative coordinates.
            if
        '''

        # using the safe algorithm.... This is not functional yet
        if safe:

            # using relative motion
            if self.coords == 'abs':
                self.rel_move()

            # going home by raising z
            line = gline('G28', com)

            # ensuring z has acceptable values values
            if z > 0:
                pass
                # raises the

            # ensuring z has good values
            if not z or z <= 0:

                # move z a different height based on type of units
                if self.coords == 'mm':
                    z = 10
                else:
                    z = 4

        else:
            # command to set the home position
            line = gline('G28', com)

            if x or x == 0:
                line.append('X' + self.settings['pos'].format(x))
            if y or y == 0:
                line.append('Y' + self.settings['pos'].format(y))
            if z or z == 0:
                line.append('Z' + self.settings['pos'].format(z))

            # recording line to mem and indicating that this is a move to write
            # the position of zeros forces the printer to return to the zero
            self.write(line, zeros(3)) # zeros is numpy
            # end of go home
        return


    # method to give command to tell printer to use absolute coordinates
    # to move
    def abs_move(self, com='Use Absolute motion'):

        # create gcode line with command and comment
        line = gline('G90', com)

        # internally recording coordinate system
        self.coords = 'abs'

        # writing line of gcode to memory
        self.write(line)
        return


    # method to give command to tell printer to use relative coordinates
    # to move
    def rel_move(self, com='Use Relative Motion'):

        # create gcode line with command and comment
        line = gline('G91', com)

        # internally recording coordinate system
        self.coords = 'rel'

        # writing line of gcode to memory
        self.write(line)
        return

    # method to reset current position
    def set_pos(self, x=None,y=None,z=None,extrude=None,com=None):
        '''
        This method does not do anything to the gcode class
        http://reprap.org/wiki/G-code#G92:_Set_Position

        Parameters:
        '''

        # creating GCODE line
        line = gline('G92', com)

        # appending parameters to line of GCODE
        if x or x == 0:
            line.append('X' + self.settings['pos'].format(x) )

        if y or y == 0:
            line.append('Y' + self.settings['pos'].format(y))

        if z or z == 0:
            line.append('Z' + self.settings['pos'].format(z))

        # writes the extrusion command to this line
        if extrude or extrude == 0:
            line.append('E' + self.settings['extrude'].format(extrude))

        # writing to memory
        self.write(line)

        return

    # Method that has different meanings depending on software
    # Hyrel def used here
    def manual_mask_off(self, com='turn off manual control printing mask'):
        '''
        Parameters:
        '''

        self.write(gline('M30',com))
        return


    # Method to tell printer to use absolute extrusion
    def abs_extrude(self, com='Absolute Extrusion Mode'):

        # create gcode command
        line = gline('M83', com)

        # should I record the volume used?

        # writing line gcode to memory
        self.write(line)


    # Method to tell printer to use relative extrusion
    def rel_extrude(self, com='Relative Extrusion Mode'):

        # create gcode command
        line = gline('M82', com)

        # should I record the volume used?

        # writing line gcode to memory
        self.write(line)
        return

    # Method to stop idle in the printer
    def stop_idle(self, com='Stop idle hold'):
        '''
        Parameters:

        '''

        self.write(gline('M84',com))
        return



    # Hyrel specific ???? tells printer to stop extruding
    def stop_extrude(self, com='Stop Extrusion'):
        '''
        Parameters:
        '''

        self.write(gline('M103',com))
        return


    # Hyrel Specific ????? turn off extruders
    def extruders_off(self, t=None,s=None, com=None):
        '''
        Parameters:

        Not sure what the values mean

        see http://hyrel3d.net/wiki/index.php/Gcode_Basics
        '''

        # Creating GCODE line
        line = gline('M104',com)

        if t or t == 0:
            line.append('T' + str(t))

        if s or s == 0:
            line.append('S' + str(s))

        # writing to memory
        self.write(line)

        return



    # Method to control the Printer fan
    def fan(self, com=None,**kwargs):
        '''
        Parameters:

        '''

        # creating GCODE line
        line = gline('M106', com)

        # formatting line and saving it to memory
        self._control_fan(line, **kwargs)

        return

    # Method to turn fan off. It is depreciated in many printers
    def fan_off(self, com=None):
        '''
        Parameters
        '''

        # writing a single line to memory
        self.write(gline('M107',com))

        return

    # method that tells printer to wait till the bed is commect temperature
    def wait_for_temp(self, temp=None, att=None, com=None):
        '''
        Parameters:

        >  TEMP: the minimum temperature target in celsius
        > ATT: the accurate temperature target

        See http://reprap.org/wiki/G-code#M190:_Wait_for_bed_temperature_to_reach_target_temp

        '''

        # Creating command
        line = gline('M190',com)

        # adding parameters values and command letters to line
        if temp:
            line.append('S'+str(temp))

        if att:
            line.append('R'+str(att))


        # saving to memory
        self.write(line)
        return


    # Method to unprime the printer
    def unprime(self, com='Unpriming Printer'):
        '''
        Parameters:

        '''

        # Writes the GCODe line
        self.write(gline('M721',com))

        return




    # Seems to be a hyrel specific GCODE command
    # http://hyrel3d.net/wiki/index.php/Gcode_Basics
    def err_report(self, time=None, com='Set error reporting interval for redundant errors'):
        '''
        Parameters:

        > Time: seconds for error reporting of redundant errors
        '''

        # creating GCODE command
        line = gline('M734', com)

        # checking if time is given
        if time or time == 0:
            line.append('S' + str(time))

        # writing line to memory
        self.write(line)

        return

    # method that tells the printer the first layer's thickness
    def first_layer_thick(self, thick=None, com='set first layer thickness'):
        '''
        Parameters:

        > THICK: the thickness of the first layer in correct distance units (mm or in)
        '''

        # Creating GCODE command
        line = gline('M756', com)

        if thick or thick == 0:
            line.append('S' + str(thick))


        # writes line to memory
        self.write(line)

        return



    # adds a new layer
    def new_layer(self, com='announce new layer'):
        line = gline('M790', com)

        # writing to memory
        self.write(line)
        return

    # end of new_layer


    # writes command for comments
    def comment(self, com):
        '''
        Parameters

        > COM: a string to be written as a comment
        '''
        line = gline(comment=com)

        # writing to memory
        self.write(line)
        return
        # end of comment


    # method that creates blank lines on the GCODE file
    def blank(self, lines=1):

        # checking the lines
        lines = int(lines)

        # creating black lines
        for i in range(lines):
            # determining how to return values
            self.write(gline())

        # end of blank
        return


    # Adds the credits
    def credits(self, in_gcode=False):

        line1 = 'This is GCODE generated with gcody version 0.1.5'
        line2 = 'Written by Ryan Zambrotta'

        # Writes the credits as a comment
        if in_gcode:
            self.comment(line1)
            self.comment(line2)
        else:
            print(line1)
            print(line2)

        # end of credits
        return



    ################################################################################
    ################################################################################
    ## Save to memory tools, Saving Tools, Calc Print time---------------------------
    ################################################################################
    ################################################################################


    # writes the output to a file
    def save(self, file):
        '''
        Parameters:

        > FILE: The file name to save to. If this has no extension, then
            a .gcode file is writen to. If there is an extension, then
            a file of that type is used
        '''

        file_type = file.split('.')

        # first case, gcode file to save to
        if len(file_type) ==  1:

            # save file name
            file = file + '.gcode'

        # opening and creating file
        with open(file,'w') as f:

            # writes all the GCODE lines at once
            f.writelines(self.code)

            # closing text file
            f.close()

        # end of store
        return



    ## IMPORTANT function here. write writes a line to memory as well as parses
    def write(self, line, move=None, time=None):

        '''
        Parameters:

        > LINE:
        > MOVE:
        > TIME:
        '''

        # increasing counter
        self.count +=1

        # checking debug mode
        # determining how to return values
        if self.debug:
            print(line)
            return
        else:
            # appending the line of GCODE to the vector of lines
            if any(move) or any(move == 0): # any is overriden by numpy import
                # records motion, time to print, and position
                self._pos_update(move, time)


            # records GCODE
            self.code.append(line.done())
            return

        # end of write
        return

    # method to print the print_time attribute in a pretty format
    # uses a helper function min2time
    # this breaks the attribute print_time into days,hours,minutes, etc.
    def time(self, printit=True, sec_tol=1e-1):

        '''
        Parameters:

        > PRINTIT: if true, the final string created is printed to screen and returned.
            If false, then the string is just returned
        > SEC_TOL: controls the precision of the seconds displayed as well as
            whether seconds will be added at all. if the number of seconds is below
            SEC_TOL, then it is not displayed. if more than 2 decimal places are needed
            scientific notation is used
        '''

        # calling helper function
        return min2time(self.print_time, printit, sec_tol) # from helper.py
    # end of time




    ######################################################################################
    ######################################################################################
    ## Visualisation tools -------------------------------------------------------------
    ## ------------------------------------------------------------------------------------
    ######################################################################################
    ######################################################################################




    # Method to visualize the printer path
    '''
    To Do:

    > DOCUMENTATION!!!!
    > Create more arguments for customizability
    > new type of visualization! one color to specify when extrude
        another color not with a legend
    > break this into several methods
    '''
    def view(self, *args, fig_title='Print Path',**kwargs):

        '''
        Parameters:


        > *args,**kwargs : are passed to matplotlib's pyplot.plot function

        > FIG_TITLE: the title given to the figure. Only used is a figure is not given to plot on

        > GIVE : this command makes the method return the figure after the path data is
                plotted. This has no effect when mayavi is the backend.
        '''

        # generating labels for the axes
        ax_labels = ['X ({})'.format(self.unit_sys),'Y ({})'.format(self.unit_sys),
                     'Z ({})'.format(self.unit_sys)]

        # function call from module visual
        fig = plot3(self.history, *args, title=fig_title,
              axis_label=ax_labels, backend=self.settings.graphics,
              **kwargs)


        return fig


    # method that has a colorbar to parameterize the time of the print
    def cbar_view(self, *args, fig_title='Printer Path', **kwargs):
        '''
        Parameters:

        see visual.py color_view for all arguments. Some are defined here. Still working on it

        '''

        # generating labels

        # generating labels for the axes
        ax_labels = ['X ({})'.format(self.unit_sys),'Y ({})'.format(self.unit_sys),
                     'Z ({})'.format(self.unit_sys)]

        # four color bar ticks
        colorbar_ticks = [0, self.t[-1]/3, 2*self.t[-1]/3, self.t[-1]]

        # generating the colorbar tick labels
        colorbar_tick_labels = ['0']

        # generating the labels by iterative over the ticks and converting them to strings
        for i in colorbar_ticks[1:]:
            colorbar_tick_labels.append('{:0.2f}'.format(i))

        # colorbar label
        colorbar_label = 'Time (min)'


        # function call from module visual
        fig = color_view(self.history, self.t, *args, fig_title=fig_title,
                   colorbar_ticks=colorbar_ticks, colorbar_tick_labels=colorbar_tick_labels,
                   colorbar_label=colorbar_label, axis_label=ax_labels,
                   backend=self.settings.graphics, **kwargs)



        return fig

    # a function to wrap the stuff needed for a live graph takes a function that returns a
    # X and Y array to be plotted, a single input i to that function is required
    def animated(self, *args, fig_title='Print Path',**kwargs):

        '''
        Parameters:

        See visual.py Some arguments are defined here though. Working on it still

        Defined here: ax_label, ax_lim, fig_title, loop
        '''

        # make a numpy array for indexing, vectorized operations, and method access
        # getting motion history
        # list comprehension to get the coordingates from self.history
        X = array([i[0] for i in self.history]) # numpy
        Y = array([i[1] for i in self.history]) # numpy
        Z = array([i[2] for i in self.history]) # numpy

        # defining the update function to needed by the plotting function
        def update(i):
            return X[0:i], Y[0:i], Z[0:i]


        # setting additional arguments
        # generating labels for the axes
        ax_labels = ['X ({})'.format(self.unit_sys),'Y ({})'.format(self.unit_sys),
                     'Z ({})'.format(self.unit_sys)]


        # Keeps aspect ratio square but can be computationally expensive for large GCODE
        # http://stackoverflow.com/questions/13685386
        # numpy array
        max_range = array([X.max()-X.min(),
                              Y.max()-Y.min(),
                              Z.max()-Z.min()]).max() / 2.0

        mean_x = X.mean()
        mean_y = Y.mean()
        mean_z = Z.mean()

        # generating the axis limits
        ax_lim = [mean_x - max_range, mean_x + max_range,
                  mean_y - max_range, mean_y + max_range,
                  mean_z - max_range, mean_z + max_range]




        # calling function from visual.py
        live_view(update, *args, ax_label=ax_labels, ax_lim=ax_lim,
                  fig_title=fig_title, loop=len(self.t)+1, **kwargs)


        return


    # method that has a slider on the bottom of the figure to animate the print path
    def slide_view(self, *args, fig_title='Printer Path', **kwargs):
        '''
        Parameters:

        See visual.py, slider_view
        '''



        # getting motion history
        # list comprehension to get the coordingates from self.history
        X = array([i[0] for i in self.history]) # numpy
        Y = array([i[1] for i in self.history]) # numpy
        Z = array([i[2] for i in self.history]) # numpy

        # defining the update function to needed by the plotting function
        def update(i):
            # when i == self.t[-1], argument == len(self.t)
            return X[0:int(i*len(self.t)/self.t[-1])], Y[0:int(i*len(self.t)/self.t[-1])], Z[0:int(i*len(self.t)/self.t[-1])]

        # defining labels:

        # setting additional arguments
        # generating labels for the axes
        ax_labels = ['X ({})'.format(self.unit_sys),'Y ({})'.format(self.unit_sys),
                     'Z ({})'.format(self.unit_sys)]


        # Keeps aspect ratio square but can be computationally expensive for large GCODE
        # http://stackoverflow.com/questions/13685386
        # numpy array
        max_range = array([X.max()-X.min(),
                              Y.max()-Y.min(),
                              Z.max()-Z.min()]).max() / 2.0

        mean_x = X.mean()
        mean_y = Y.mean()
        mean_z = Z.mean()

        # generating the axis limits
        ax_lim = [mean_x - max_range, mean_x + max_range,
                  mean_y - max_range, mean_y + max_range,
                  mean_z - max_range, mean_z + max_range]


        # generating the slider labels
        slider_label = 'Time (min)'
        slider_range = [0, self.t[-1]]
        slider_dx = self.t[-1]/len(self.t)

        # calling function from visual.py
        slider_view(update, *args ,slide_label=slider_label, slide_range=slider_range,
                    ax_lim=ax_lim, ax_label=ax_labels, fig_title=fig_title, slide_dx=slider_dx,
                    **kwargs)

        return


    ######################################################################################
    ######################################################################################
    ## Hidden methods to handle internal processes---------------------------------------
    ## ------------------------------------------------------------------------------------
    ######################################################################################
    ######################################################################################

    # hidden method to format the GCODE move command
    def _move_format(self, line,pos=None,x=None,y=None,z=None,speed=None,extrude=None,check_end=None,write=True):
        '''
        Parameters:

        > LINE: the gline that already contains the GCODE command

        > X: The x coordinate to move the print head to. X can be an int,float, or array
            of shape (n,) or (n,3). If shape is (n,), then each element is used
            sequentially as the x coordinate for each motion (each element in the array).
            If X has shape (n,3), then each column is defined as x,y,z and each row is a
            subsequent movement.
        > Y: the y coordinate to move the print head to. Behaves the same as X except for
            that only arrays of shape (n,) can be passed.
        > Z: the z coordinate to move the print head to. Behaves the same as X except for
            that only arrays of shape (n,) can be passed.
        > SPEED: The speed to move the print head for this motion. This input should
            be in the same units as the attribute UNIT_SYS
        > EXTRUDE: The volume to extrude for this motion.... NEED MORE HERE
        > CHECK_END: determines whether the printer checks if an endstop was hit. Default
            to '0'. Options are '0', '1','2'. '1' makes printer check. '2' is more
            machine specific.
        > WRITE: determines whether to write the line to memory or two return the pos and
            line instead
        '''

        # appending parameters to line of GCODE
        if x or x == 0:
            line.append('X' + self.settings['pos'].format(x) )
            # updating position
            pos[0] = x

        if y or y == 0:
            line.append('Y' + self.settings['pos'].format(y))
            # updating position
            pos[1] = y

        if z or z == 0:
            line.append('Z' + self.settings['pos'].format(z))
            # updating position
            pos[2] = z

        # writes the speed command
        if speed:
            # calls a hidden function to format the speed string
            # and two adjust attributes
            line.append('F' + self._speed(speed))

        # writes the extrusion command to this line
        if extrude or extrude == 0:
            line.append('E' + self.settings['extrude'].format(extrude))

        # writes command to check if an end point was hit. this defaults to not checking
        if check_end:
            line.append('S' + check_end)

        # determining how to return values or to save the GCODE lines to memory
        if write:
            # writing to memory
            self.write(line,pos)
        else:
            # returning both values
            return line, pos



    # method to format the speed command for the move functions and recording the
    # speed as an internal attribute unit_sys.
    def _speed(self, v):

        # update internal record of speed
        if self.unit_sys == 'mm':
            # convert units of milimeters per sec to milimeters per minute
            self.print_speed = mmps2mmpm(v)
        else:
            # convert units of inches per sec to inches per meter
            self.print_speed = inps2inpm(v)

        # returning the formated string of the speed
        return self.settings['speed'].format(self.print_speed)



    # method to internally record the time for motion. called in _pos_update
    def _time(self, time=None):

        '''
        Calculates the time of motion, independant of coordinate systems

        Parameters:

        > TIME: if time is given, this time is added to the running total
            and to the
        '''

        # distance is the 2-norm distance between the two points
        distance = norm(self.current_pos - self.previous_pos) # from numpy.linalg

        # checking if print_speed has been set to non_zero
        if self.print_speed != 0:

            # if time is given, the value is added, not calculated
            if time:
                self.print_time += time
            else:
                # recording the time taken to move in minutes
                self.print_time += distance/self.print_speed

        # if not, a warning is raised that time will be inf
        else:
            # only printing warning once
            if self.count == 1:
                raise Warning('Print speed not set. Print Times are Inf')

        # adds an element to a vector of time
        self.t.append(self.print_time)

        return



    # method to internally handle updating the previous and current position, the
    # to the time to move, and recording the history of motion for plotting
    def _pos_update(self, pos, time=None):
        '''
        Parameters:

        > POS: the newly moved to position.  This is always recorded in absolute
            coordinates
        '''

        # reassigning positions of the print head based on motion given by po
        self.previous_pos = self.current_pos.copy() # passing array by copy

        # addds the current position to the motion history
        if self.coords == 'abs':

            # recording new position
            self.current_pos = pos.copy()

        else:
            # records position for relative coordinates. Position is in abs coordinates
            self.current_pos += pos

        # recording motion
        # need to pass a copy because a pointer is passed by default.
        # this would mean that self.history would just be a list of the same pointer
        self.history.append(self.current_pos.copy())


        # updates the time taken to move the print head
        self._time(time)

        return

    # Method to control the fan parameters
    def _control_fan(self,line,fan_speed=None, fan_n=None, invert_sig=None, fan_freq=None,
                     set_min_speed=None, blip_time=None, select_heaters=None, restore_speed=None,
                     set_trig_temp=None, write=True):

        '''
        Parameters:

        See http://reprap.org/wiki/G-code#M106:_Fan_On
        '''


        if fan_speed or fan_speed == 0:
            line.append('S' + str(fan_speed))

        if fan_n or fan_n==0:
            line.append('P' + str(fan_n))

        if invert_sig:
            line.append('I' + str(invert_sig))

        if fan_freq or fan_freq == 0:
            line.append('F' + str(fan_freq))

        if set_min_speed or set_min_speed==0:
            line.append('L' + str(set_min_speed))

        if blip_time or blip_time == 0:
            line.append('B' + str(blip_time))

        if select_heaters or select_heaters==0:
            line.append('H' + str(select_heaters))

        if restore_speed or restore_speed==0:
            line.append('R' + str(restore_speed))

        if set_trig_temp:
            line.append('T' + str(set_trig_temp))

        # determining how to return the values
        if write:
            self.write(line)
            return
        else:
            return line




    # functions that give the printing options of the GCODE
    def __repr__(self):
        # creates a print object and returns that
        return ''.join(self.code)

    def __str__(self):
        # creates a print object and returns that
        return ''.join(self.code)

    # gives [] indexing gives access to the gcode methods as identified by the
    # actual GCODE commands. This makes reading GCODE easier
    def __getitem__(self, index):
        return self.gcode_methods[index]

    # gives built in len function access to self.code
    def __len__(self):
        return self.count
