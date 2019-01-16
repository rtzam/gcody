import gcody as g

# a file to read 
file = r'C:\Users\Ryan\Desktop\GithubFiles\gcody\demo\elefante_small.gcode'

# setting graphics backend to be mayavi
settings = g.gsettings(graphics='mayavi')

# reading gcode file
elefante = g.read(file, settings=settings)


# standard viewing of gcode
elefante.view(elefante.t,colormap='jet', figsize=(1500,1500))


# viewing the gcode
elefante.cbar_view(figsize=(1500,1500))







