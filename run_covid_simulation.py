
PROGRAM_EXPLANATION = """
run_covid_simulation.py directs the simulation to be ran either in a graphical user interface (GUI) or from a text 
input file. Both output a series of plots and a .gif of covid transmission through an office. See README for guidance on 
valid inputs.

Commands:
    --help      Display this program explanation.
    --GUI       Run the simulation from a GUI that can be used to input parameters and display results.
    
Inputs: <simulation_inputs.txt>    When no commands used, a text file containing a valid dictionary of parameter 
                                   values can be input to run the simulation without a GUI, potentially for batch tests. 
"""


def main(*arguments):
    """Checks commands valid and selects either GUI or .txt for simulation."""
    if len(arguments) > 1:
        print('Error: only one input allowed. Use --help for program explanation.')
    elif not arguments or arguments[0] == '--help':
        print(PROGRAM_EXPLANATION)
    elif len(arguments) == 1 and arguments[0] == '--GUI':
        # Run the simulation through the GUI interface
        import GUI
        GUI.GUI()
    elif len(arguments) == 1 and arguments[0].endswith('txt'):
        # Read in text file input parameters and run the simulation without GUI
        file = open(arguments[0], 'r')
        contents = file.read()
        try:
            # Import parameters from text file as dictionary
            parameters = ast.literal_eval(contents)
        except SyntaxError:
            print('Error: dictionary syntax invalid.')
            raise SystemExit
        finally:
            file.closed

        # Run simulation and save outputs
        sim = simulation.main(parameters)
        simulation.save_outputs(sim)
    else:
        print(PROGRAM_EXPLANATION)


if __name__ == "__main__":
    """Run the simulation from the command line"""
    # Read in arguments and run main body

    # External modules
    import sys
    import ast

    # Directory modules
    import simulation

    arguments = sys.argv[1:]
    main(*arguments)
