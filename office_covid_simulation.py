

PROGRAM_EXPLANATION = """

TO BE UPDATED - currently the same as simulation

simulation.py
Designed and written by Adam Honnywill and James Hawke, predominantly through "pair coding"
April 2021

This script runs simulations of coronavirus transmission in an office to investigate the effects of various
parameters, such as wearing or social distancing. The script may be used to:

    1. Show an animation of the simulation on screen
    2. Create a video of a simulation
    3. Show a plot of different stages of the epidemic
    4. Save a plot to a file

This is done using code in this script, which in turn uses uses classes in other scripts:

    1. office.py            # to track the movement of people at any given time in the office space
    2. person.py            # to instantiate people in the office
    3. GUI.py               # to perform GUI based parameter input
    4. transmission.py      # to update the infection status of people upon interaction

The command line interface to the script allows for user input parameters to be input either from a GUI or a
text file, such that no code needs changing between simulations:

    $ python simulation.py               # run simulation with with text file input parameters
    $ python simulation.py --GUI         # run simulation with with GUI input parameters
    $ python simulation.py --help        # show all command line options

In order to run this script, one or two input files must be present in the directory:

    1. office_array.xls     # always
    2. input_parameters.txt # if the --GUI flag is not called

It is also possible to create a video of the animation (if you install
ffmpeg):

    $ python simulator.py --file=simulation.mp4

NOTE: You need to install ffmpeg for the above to work. The ffmpeg program
must also be on PATH.
"""


def main(*arguments):
    if len(arguments) > 1:
        print('Error: only one input allowed. Use --help for programme explanation')
    elif not arguments or arguments[0] == '--help':
        print(PROGRAM_EXPLANATION)
        return
    elif len(arguments) == 1 and arguments[0] == 'GUI':
        import GUI
        GUI.main()
    elif len(arguments) == 1 and arguments[0] == 'GUI':
        import GUI
        GUI.main()
    elif len(arguments) == 1 and arguments[0].endswith('txt'):
        file = open(arguments[0], 'r')
        contents = file.read()
        import ast
        parameters = ast.literal_eval(contents)
        file.close()
        import simulation
        sim = simulation.main(parameters)
        simulation.save_outputs(sim)
        


if __name__ == "__main__":
    import sys
    arguments = sys.argv[1:]
    main(*arguments)
