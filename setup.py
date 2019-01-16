# File to allow for the PyPI setup
# https://pypi.org/

# imports needed
from setuptools import setup, find_packages


# loading the README.md file as the long description
with open('README.rst','r') as rm:
    long_description = rm.read()
    rm.close()

# getting version number only change in one place
with open('version.txt', 'r') as f:
    version_num = f.read()
    f.close()


# using setup to describe the module
setup(
    name = 'gcody',
    version = version_num,
    packages = find_packages(),

    # generic metadata
    author = 'Ryan Zambrotta',
    author_email = 'rtzamis2@gmail.com',
    url='https://github.com/rtZamb/gcody',
    description = 'A package to read, write, and visualize GCODE',
    long_description = long_description,
    long_description_content_type="text/markdown",
    license = 'MIT',
    keywords = ['GCODE','3D Printing','visualiziation','CNC'],
    package_data = {'':['*.txt', '*.md']},
    install_requires = ['numpy','matplotlib']
    
    )
