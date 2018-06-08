# Class of a basic line of gcode



# base class that represents a single line of gcode
class gline():

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
        '''
        Parameters:

        > TEXT: the text to add to the end of the line.

        * Notes: each command is added with a space if the line is not empty
        '''

        # checking to see if line is empty before adding space to append
        if self.line == '':
            self.line += str(text)

        # else a space is added to seperate words
        else:
            self.line += ' ' + str(text)
        


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
