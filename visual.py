# Module that contains GCODE visualization tools to be called by the class gcode

# Needed imports
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style


def plot3(history, *args, fig_title=None, give=False,plot_style='default',
         axis_label=None, make_square=True, **kwargs):
        
    '''
    Parameters:
        
    > *args,**kwargs : are passed to matplotlib's pyplot.plot function

    > FIG_TITLE: the title given to the figure. Only used is a figure is not given to plot on

    > GIVE : this command makes the method return the figure after the path data is
            plotted.
    '''

    # creating figure
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')

    # getting motion history
    X = history[:, 0]
    Y = history[:, 1]
    Z = history[:, 2]

    # To Do add optional label to the first point
    # Plots the 3 past printer positions on figure
    ax.plot(X, Y, Z, *args, **kwargs)

    if make_square:
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

    # labeling figure axes 
    if axis_label:
        ax.set_xlabel(axis_label[0])
        ax.set_ylabel(axis_label[1])
        ax.set_zlabel(axis_label[2])

    # sets the figure title
    if fig_title:
        plt.title(fig_title)


    # determines whether to show the figure or to return it
    if give:
        return ax
    else:
        # showing figure
        plt.show()

    # end of view
    return



'''
To Do:

add option of labeling the start and stopping point
'''

# using time to color the line representing printer motion
# help from https://matplotlib.org/gallery/lines_bars_and_markers/multicolored_line.html
def color_view(history, time, *args, cmap='jet', axis_label=None, fig_title=None,
               plot_style='default', colorbar_ticks=None, colorbar_tick_labels=None,
               colorbar_label=None,give=False,**kwargs):

    '''
    Parameters:

    > HISTORY:
    > ARGS:
    > CMAP:
    > AXIS_LABEL:
    > FIG_TITLE:
    > PLOT_STYLE:
    > COLORBAR_TICKS:
    > COLORBAR_TICK_LABELS:
    > COLORBAR_LABEL
    > GIVE:
    > KWARGS:
    '''

    # Type Checking the inputs

    # setting matplotlib plot style
    style.use(plot_style)

    # creating figure
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_aspect('equal')

    # getting motion history
    X = history[:, 0]
    Y = history[:, 1]
    Z = history[:, 2]

    # creating the color scheme to parametricise this plot in time
    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(0,time[-1])


    # creating CM object that contains the method to get colors in the map
    color_map = plt.cm.ScalarMappable(norm, cmap)

    # creating array of RGBA colors to pass when plotting
    colors = color_map.to_rgba(time)

    # adding colorbar to figure
    color_map.set_array(time) # trick to make this work from:
    # https://stackoverflow.com/questions/8342549/matplotlib-add-colorbar-to-a-sequence-of-line-plots

    # adding colorbar with the given ticks
    if colorbar_ticks:
        # actually adding color bar with given_ticks
        colorbar = fig.colorbar(color_map, pad=0.09,
                                ticks=colorbar_ticks)

    # else, use default which does calculations on time
    else:
        # actually adding color bar with 3 tick marks
        colorbar = fig.colorbar(color_map, pad=0.09,
                                ticks=[0,time[-1]/2,time[-1]])
        

    # adding tick labels to color bar if they are given. Else nothing is created
    if colorbar_tick_labels:
        colorbar.ax.set_yticklabels(colorbar_tick_labels)


    # setting label of color bar
    if colorbar_label:
        colorbar.set_label(colorbar_label)
    

    # Plots the 3 past printer positions on figure parameterized by time
    for i in range(1,len(X)):
        ax.plot(X[i-1:i+1], Y[i-1:i+1], Z[i-1:i+1], *args,
                color=colors[i,:], **kwargs)


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

    # labeling figure axes 
    if axis_label:
        ax.set_xlabel(axis_label[0])
        ax.set_ylabel(axis_label[1])
        ax.set_zlabel(axis_label[2])

    # adding figure title
    if fig_title:
        plt.title(fig_title)


    # determines whether to show the figure or to return it
    if give:
        return ax
    else:
        # showing figure
        plt.show()

    # end of view
    return




# a function to wrap the stuff needed for a live graph takes a function that returns a
# X and Y array to be plotted, a single input i to that function is required
def live_view(animate, *args, loop=60, ax_lim=None, ax_label=None,
              fig_title=None, save_file=None, writer='pillow',refresh=100,
              plot_style='default',show=True,**kwargs):

    '''
    Parameters:
    
    > ANIMATE: A function that takes a single integer input starting from zero. This
        function must return x,y,z to be plotted
    > ARGS:
    > LOOP:
    > AX_LIM: x,y,z axis limits in x,y,z order from low to high
    > AX_LABEL: a list-like object that contains strings for the x,y,z labels in that order
    > FIG_TITLE:
    > SAVE_FILE:
    > ANIMATE:
    > COLOR:
    > REFRESH:
    > PLOT_STYLE:
    > KWARGS:
    '''

    # need imports
    import matplotlib.animation as animation
    
    # maplotlib style to use
    style.use(plot_style)

    # creating new figure to plot on
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')

    # creates the animation
    def animate_loop(i):

        # Makes loop cycle so that it restarts after it's full length is reached
        i = i % (loop - 1)

        # calls the animate function
        x,y,z = animate(i) 
        
        # cleans old drawing off screen. computationally light
        ax.clear()
        
        # redraws stuff on to plot
        ax.plot(x,y,z, *args,**kwargs)

        # setting axis sizes
        if ax_lim != None:
            ax.set_xlim(ax_lim[0], ax_lim[1])
            ax.set_ylim(ax_lim[2], ax_lim[3])
            ax.set_zlim(ax_lim[4], ax_lim[5])

        # labeling axes
        if ax_label != None:
            ax.set_xlabel(ax_lim[0])
            ax.set_ylabel(ax_lim[1])
            ax.set_zlabel(ax_lim[2])

        # setting figure title
        if fig_title:
            plt.title(fig_title)
        

    # animation function from matplotlib
    # arguments are where to draw, which drawing function to use, and how often to redraw
    ani = animation.FuncAnimation(fig, animate_loop, interval=refresh)

    # if a save file is passed, the animation is saved to the file
    if save_file:
        ani.save(save_file, writer=writer) # saves to an mp4 file
        

    # calling figure to screen
    if show:
        plt.show()

    # end of the live_view method
    return


# help from
# https://matplotlib.org/gallery/widgets/slider_demo.html
def slider_view(initial, update, *args, slide_geo=[0.25, 0.1, 0.65, 0.03],
                slide_label=None, slide_color='w', slide_range=[0,10], slide_0=0.0,
                slide_dx=1, ax_lim=None,plot_style='default', **kwargs ):

    '''
    Parameters:

    > INITIAL: the first values to be plotted. should have shape (n,3)
    > UPDATE: a function that takes the slider value and dr
    > ARGS:
    > SLIDE_GEO: default to [0.25, 0.1, 0.65, 0.03]
    > SLIDE_LABEL:
    > SLIDE_COLOR: default to white
    > SLIDE_0 = default to zero. inital value of the slider
    > SLIDE_DX: default to 1. increment of the slider motion
    > PLOT_STYLE:
    > KWARGS:
    '''

    # extra import
    from matplotlib.widgets import Slider

    # maplotlib style to use
    style.use(plot_style)

    # creating new figure to plot on
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_aspect('equal')

    # inital data
    data = update(0)

    # plotting inital data on the figure
    l, = plt.plot(*data,*args)

    # setting axes for the first time
    ax.set_xlim(ax_lim[0], ax_lim[1])
    ax.set_ylim(ax_lim[2], ax_lim[3])
    ax.set_zlim(ax_lim[4], ax_lim[5])

    # adjusting to offset for the slider
    plt.subplots_adjust(bottom=0.25)

    # defining the slider geometry and color:
    time_ax = plt.axes(slide_geo, facecolor=slide_color)
    
    # adding the slider to the figure:
    time_slider = Slider(time_ax, slide_label, valmin=slide_range[0],
                         valmax=slide_range[1], valinit=slide_0, valstep=slide_dx)

    # calling update function to set the new plotted values
    def slide(i):

        # calling update function to give new values
        x,y,z = update(i)

        # setting new values
        l.set_xdata(x)
        l.set_ydata(y)
        l.set_3d_properties(z)

        # setting axis sizes
        if ax_lim != None:
            ax.set_xlim(ax_lim[0], ax_lim[1])
            ax.set_ylim(ax_lim[2], ax_lim[3])
            ax.set_zlim(ax_lim[4], ax_lim[5])
        

        # drawing the new values to the figure
        fig.canvas.draw_idle()


    # tells the slider to use the slide function to update the figure
    time_slider.on_changed(slide)

    # showing the figure
    plt.show()




####################################################################################
####################################################################################
# Testing the functions above:
####################################################################################
####################################################################################

##import numpy as np
##
### animation function
##def anim(i):
##    # creates the parameter
##    t = np.linspace(0,i/5, 1.5*i+50)
##
##    # creating x and y variables
##    x, y = np.sin(t), np.sin(2*t)
##    return x,y, x**2 + y**2 
##
### parameter
##t = np.linspace(0,6.28,200) # this is a single period of the sin function
##
##x = np.sin(t)
##y = np.sin(2*t)
##z = x**3 + y**2
##
### need the transpose to format data properly
##data = np.array([x,y,z]).T
##
### the axes sizes
##ax_l = [-1,1,-1,1,0,2]
##
### Simple view function
##view(data) # this works

# color view function with line colored by time
#color_view(data,t)

# live view of the function. This needs an animate function
#live_view(anim, loop=35, ax_lim=ax_l)

# slider view function
#slider_view(data,anim, ax_lim=ax_l,slide_range=[0,32], slide_dx=0.5)
































    
    


