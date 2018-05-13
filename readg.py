'''
Module that contains a class to parse through GCODE and recreate what the
code does!

Written by Ryan Zambrotta
'''
from .gcode import gcode


# Contains a function to read GCODE from a file and create a gcode object that contains
# the same information
def read(file=None, **kwargs):
    '''
    Parameters:

    > FILE: if a file is given, then it is read from or a list
        where each element is each line of GCODE
    > KWARGS: these are passed to an empty gcode object when it is constructed
    '''

    # list that will hold all the lines in the file given
    lines = []


    # open give file as read only
    if isinstance(file, str):
        f = open(file, 'r')

    # This should just pass a pointer so should be quick and saves a lot of typing
    elif isinstance(file, list):
        f = text
    else:
        raise RuntimeError('Unable to read input data of type {}'.format(type(file)))



    # creating an empty GCODE object to then populate
    code = gcode(**kwargs)

    
    # iterating over all lines in file f
    for line in f:

        # removes whitespace from the beginning and end of the string
        line = line.lstrip().rstrip('\n ')

        # if the line is a blank line
        if line == '':
            
            # manybe should ignore blank lines when reading?
            # writing a blank line
            code.blank()

            # next iteration, new line
            continue

        # G related commands. These have several arguments
        if line[0] == 'G':

            # structure storing all the arguments after the G command in this line
            k = {}

            # breaks up the line into stuff before and after comment
            try:
                # breaks up line into two string
                commands, comment = line.split(';', 1)

                # removing extra spaces from the comment (only can have spaces on the right side)
                comment = comment.lstrip()
                commands = commands.rstrip()
                
            except Exception as e:
                commands = line
                comment = None

            # strinping extra spaces from commands and breaking it into seperate commands
            commands = commands.split(' ')
            
            # iterating over all elements in a single line of GCODE
            for i in commands[1:]:
                
                # iterating over all possibilities
                # checking for x coord
                if i[0] == 'X':
                    k['x'] = float(i[1:])
                    
                # checking for y coord
                elif i[0] == 'Y':
                    k['y'] = float(i[1:])

                # checking for z coord
                elif i[0] == 'Z':
                    k['z'] = float(i[1:])

                # checking for speed
                elif i[0] == 'F':
                    # the division by 60 accounts for unit conversions in the
                    # move function
                    k['speed'] = float(i[1:])/60

                # checking for extrusion
                elif i[0] == 'E':
                    k['extrude'] = float(i[1:])

                # checking for check end hit
                elif i[0] == 'S':
                    k['check_end'] = i[1:]

                # ignoring unknown commands
                else:
                    print(line)
                    print(commands)
                    
                    raise Warning('Unknown parameter, {}, passed to command {}'.format(i[2:],i[0:2]))
                    

            # passing the G command to code and adding the arguments
            try:
                code[commands[0]](**k,com=comment)

            except Exception as e:
                raise TypeError(e)

            # end of line. moving to next one
            continue
            
        

        # M related commands. These typically do not have arguments
        elif line[0] == 'M':

            # splitting by comment
            try:
                # break line up into 2 strings
                command, comment = line.split(';', 1)

                # removing extra spaces
                comment = comment.lstrip()
                command = command.rstrip()

            # if exception, there is no comment and only commands
            except Exception as e:
                command = line
                comment = None


            # creating dictionary to store keyword arguments
            k = {}

            # breaking up commands into a list of strings
            command = command.split(' ')
            

            # if the M command is this, then the following arugments are needed:
            # Fan speed commands
            if command[0] == 'M106':
                
                # parsing through parameters:
                for i in command[1:]:

                    if i[0] == 'S':
                        k['fan_speed'] = i[1:]

                    elif i[0] == 'P':
                        k['fan_n'] = i[1:]

                    elif i[0] == 'I':
                        k['invert_sig'] = i[1:]

                    elif i[0] == 'F':
                        k['fan_freq'] = i[1:]

                    elif i[0] == 'L':
                        k['set_min_speed'] = i[1:]

                    elif i[0] == 'B':
                        k['blip_time'] = i[1:]

                    elif i[0] == 'H':
                        k['select_heaters'] = i[1:]

                    elif i[0] == 'R':
                        k['restore_speed'] = i[1:]

                    elif i[0] == 'T':
                        k['set_trig_temp'] = i[1:]
            

            # command for waiting till bed is certain temperature
            elif command[0] == 'M190':

                # parsing through parameters:
                for i in command[1:]:

                    if i[0] == 'S':
                        k['temp'] = i[1:]
                        
                    elif i[0] == 'R':
                        k['att'] = i[1:]


            # Hyrel Command for error reporting
            elif command[0] == 'M734':

                # iterating over all commands and checking for parameters
                for i in command[1:]:

                    if i[0] == 'S':
                        k['time'] = i[1:]

            # Hyrel command to turn extruders off
            elif command[0] == 'M104':

                # iterating over all commands and checking for parameters
                for i in command[1:]:

                    if i[0] == 'S':
                        k['s'] = i[1:]

                    elif i[0] == 'T':
                        k['t'] = i[1:]
                        

            ############################################################                
            # pass the command to the gcode object, this runs the command
            code[command[0]](**k,com=comment)

            # next iteration, new line
            continue

        # if the line is a comment line
        elif line[0] == ';':
            
            # passing to comment function after removing unneeded spaces
            code.comment(line[1:].lstrip())

            # next iteration, new line
            continue
        

        else:
            raise Warning('Unknown command {}, Skipping command'.format(line))

    # closing file
    f.close()

    # returning the filled gcode object
    return code
