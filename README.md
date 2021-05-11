# FCP_project James Hawke, Adam Honnywill, James Irvin, Alex Straw

This script runs simulations of coronavirus transmission in an office to investigate the effects of various
parameters, such as wearing a mask or social distancing. The script may be used to:

    1. Show an animation of the simulation on screen
	2. Save plots of each frame of the simulation
    3. Create a gif of a simulation
    

The following modules have been written to achieve this:

    1. office.py            # to track the movement of people at any given time in the office space
    2. person.py            # to instantiate people in the office
    3. GUI.py               # to perform GUI based parameter input
    4. transmission.py      # to update the infection status of people upon interaction
    5. simulation.py	    # to connect modules 1 to 4 to run move and infect people in the office

The command line interface to the script allows for user input parameters to be input either from a GUI or a
text file, such that no code needs changing between simulations:

    $ python run_covid_simulation.py               # run simulation with with text file input parameters
    $ python run_covid_simulation.py --GUI         # run simulation with with GUI input parameters
    $ python run_covid_simulation.py --help        # show all command line options

In order to run this script, one or two input files must be present in the directory:

    1.  office_array.xls     # always
		The office array must only contain values specfied in the key tab of office_array.xls.
		There is no limit on the number of desk (D) and task (T) locations you can add.
		Wall values (0s) must form a complete perimeter around the office.
		There must be no empty cells within the walls.
		Diagonal walls must have touching faces e.g.
		Good:		Bad:
		0000000	     0000000
		0     0      0     0
		00    0       0    0
		 00   0        0   0
		  00000         0000
		
		
		
    2.  input_parameters.txt # if the --GUI flag is not called
		input_parameters must be a python dictionary and contain all parameters detailed below:
		{'Maximum Age': 65,
		 'Minimum Age': 20,
		 'Mask Adherence': 70,
		 'Social Distancing Adherence': 50,
		 'Office Plan': 0,
		 'Virality': 50,
		 'Number of People': 30,
		 'Number of Infected': 10,
		 'Simulation Duration': 50}

Some modules used by this project may not be included in your python environment.
Please ensure you have the following modules installed:

imageio
itertools
joblib
matplotlib
os
pandas
pathfinding
pickle
random
scipy
shutil
sys
time
tkinter
xlrd





