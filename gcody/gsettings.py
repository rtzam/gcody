# Class that controls the formatting of the number when gcode is written

# class that stores settings for the gcode class
class gsettings():

    # init method contains all the default options
    def __init__(self, pos_str='{:0.4f}',speed_str='{:0.0f}',
                 extrude_str='{:0.4f}', graphics='matplotlib'):

        # assigning values to memory
        # these are the string formatters when writing numbers to gcode
        self.lib = {'pos':pos_str, 'extrude':extrude_str, 'speed':speed_str}

        # this is the graphics backend choice to avoid specifying
        # it everytime for different types of figures
        self.graphics = graphics

        # end of init
        return

    # method to format a string that provides checks on input arguments
    def format(self, lib_arg, x):
        return self.lib[lib_arg].format(x)

    # methods to use builtin functions ----------------------------------------------
    def __repr__(self):
        return str(self.lib)
    def __str__(self):
        return str(self.lib)
    def __len__(self):
        return len(self.lib)
    def __getitem__(self, lib_arg):
        return self.lib[lib_arg]
