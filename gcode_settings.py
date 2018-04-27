# Class that controls the formatting of the number when gcode is written

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
