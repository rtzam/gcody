# File contains many helper function for gcode
from numpy import array, floor, log10



## ----------------------------------------------------------------------------------------
# function that takes a value of time in specified units
# and converts it to a string of years, weeks, days, hours, minutes, and seconds.
def min2time(m=1, printit=True, sec_tol=1e-1):

    '''
    Parameters:

    > M: the number of minutes. must be an integer or a float. This gets
        broken down into time components of years, weeks, days, hours,
        minutes, and seconds.
    > PRINTIT: if true, the final string created is printed to screen and returned.
        If false, then the string is just returned
    > SEC_TOL: controls the precision of the seconds displayed as well as
        whether seconds will be added at all. if the number of seconds is below
        SEC_TOL, then it is not displayed. if more than 2 decimal places are needed
        scientific notation is used
    '''


    # Handling simply, fast cases first
    if m < 1:
        print('{:0.1f} sec'.format(m))
        return

    elif m < 60:
        print('{} min'.format(floor(m)), # floor from numpy
          '{:0.1f} sec'.format((m%1) * 60))
        return

    
    
    # minutes in a year, week, day, hour 
    min_in_x = array([524160, 10080, 1440, 60, 1]) # numpy

    # untis of of time singular and plural forms
    units_s = ['year','week','day','hour','min']
    units_p = ['years','weeks','days','hours','min']

    # stores the string representation of the time in minutes
    t = ''

    # iterates and creates string for everything except seconds
    for i in range(len(min_in_x)):

        # checks how many time units for this iteration
        n = m / min_in_x[i]
        
        if  n > 1:

            # using plural form of units
            if n > 2:
                # adding the number of years to t
                t += '{} {} '.format(int(floor(n)), units_p[i]) # floor from numpy
            else:
                # adding the number of years to t with sigular form
                t += '{} {} '.format(int(floor(n)), units_s[i]) # floor from numpy
                
            

            # removing the number of time units from m
            m = m % min_in_x[i]

            # going to next iteration
            continue

    # assuming that the above code has run that applys % to m
    # adding on number of seconds
    secs = m*60

    # putting number of seconds on the string
    if secs > sec_tol:

        # formatting the seconds string

        # by building the format
        decimal_places = int(abs(log10(sec_tol))) # log10 from numpy

        # if there are few decimal places desired, use float formatting
        if decimal_places <= 2 :
            str_format = ':0.{}f'.format(decimal_places)

        # else use scientific notation
        else:
             str_format = ':0.{}e'.format(decimal_places)
        
            
        # creating the string that has the number format
        sec_str = '{{{}}} sec'.format(str_format)

        # actually formatting the string
        t += sec_str.format(secs)

    # forcing string to have no trailing spaces
    t = t.rstrip()

    # returning string based on parameters
    if printit:
        print(t)
        return t
    else:
        return t
# end of method print_time



## --------------------------------------------------------------------------------------
## unit conversion

# converts milimeters per second in GCODE standard milimeters per minute
def mmps2mmpm(v=1):
    return v*60
# converting milimeters per minute in GCODE standard milimeters per second
def mmpm2mmps(v=1):
    return v/60
# convert milimeters to inchs
def in2mm(v=1):
    return v*25.4
# convert inches to milimeters
def mm2in(v=1):
    return v/25.4
# convert units of inches per second to inches per minute
def inps2inpm(v=1):
    return v*60
# converting inches per minute in GCODE standard inches per second
def inpm2inps(v=1):
    return v/60
# convert minutes to seconds
def min2sec(t=1):
    return t*60
# convert seconds to minutes
def sec2min(t=1):
    return t/60
