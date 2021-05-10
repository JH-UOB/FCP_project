"""

GUI.py
Designed and written by James Irvin
May 2021

This script contains a function which creates a GUI that can be used to view and the office layout and control input
parameters to simulation.py.

Used by simulation.py.
"""

# Import modules
import matplotlib.backends.backend_tkagg
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import simulation
import time
from office import Office
import pickle
import os
import shutil
import sys


# Main body
def GUI():
    """This function is used to generate a Tkinter Graphical User Interface (GUI) which allows the user to change input
    parameters using widgets.

        The GUI is also used to present animated results from simulation.py as a matplotlib plot.

        The following parameters can be changed within the "parameters" dictionary [widget]

            "Number of people" - The number of people in the office [spin box]
            "Number of infected people" - The number of infected people [spin box]
            "Maximum Age" - Maximum possible age of people in the office [slider]
            "Minimum Age" - Minimum possible age of people in the office [slider]
            "Mask Adherence" - Percentage of people who wear a face mask [slider]
            "Virality" - Percentage of virality [slider]
            "Social Distancing Adherence" - Percentage of people who adhere to social distancing measures [slider]
            "Office Plan" - Which floor of the office is simulated from the 4 choices [Listbox]
            "Simulation duration" - Number of movement interactions to model simulation over [slider]

        Once the user has specified their parameters they  can begin the simulation by pressing the "Begin Simulation"
        button - This passes on the parameters to simulation.py.

        The simulated office space is then shown for each discrete time event.

        Additionally there is a button to save the Animation which saves the Matplotlib frames as a GIF

        The function is seperated into the following subsections:

            - (1) Functions which handle callbacks *Note: These fuctions must be nested within GUI for the widget
                  callbacks to work correctly*
            - (2) Initialising the parameters dictionary.
            - (3) Setup of the GUI window, frames and figure and toolbar.
            - (4) Setup GUI labels for parameters
            - (5) Setup of widgets
        """

    # (1) Functions which handle callbacks

    def update_lbl_MaxAge(Max_Age):
        """Update the Max Age label and check that max age exceeds min age.
        If this is not true then the begin simulation button is disabled"""
        try:
            Min_Age = int(float((Min_Age_Slider.get())))  # Get the current value of min age
        except:
            # This is required as the max age slider is initialised before the min slider - this means for the first...
            # loop the min age slider doesnt exist so in this instance min age is defined from parameters.
            Min_Age = parameters['Minimum Age']
        Max_Age = int(float((Max_Age)))  # Convert from Tkinter IntVar() to Int
        Max_Age_label['text'] = "Maximum age: " + str(Max_Age) + " years old"  # Update max age label
        parameters.update({"Maximum Age": Max_Age})  # Update max age within parameters
        if Min_Age > Max_Age:
            switch_off_Begin_sim_button_state()  # disable begin sim button
        else:
            switch_on_Begin_sim_button_state()  # enable begin sim button

    def update_lbl_MinAge(Min_Age):
        """Update the Min Age label and check that max age exceeds min age.
                If this is not true then the begin simulation button is disabled"""
        Min_Age = int(float((Min_Age)))  # Convert from Tkinter IntVar() to Int
        Max_Age = int(float((Max_Age_Slider.get())))  # Get the current value of max age
        Min_Age_label['text'] = "Minimum age: " + str(Min_Age) + " years old"  # Update min age label
        parameters.update({"Minimum Age": Min_Age})  # Update min age within parameters
        if Min_Age > Max_Age:
            switch_off_Begin_sim_button_state()
        else:
            switch_on_Begin_sim_button_state()

    def update_lbl_MA(Mask_Adh):
        """Update the Mask Adherence label"""
        Mask_Adh = int(float((Mask_Adh)))  # Convert from Tkinter IntVar() to Int
        MA_label['text'] = "Mask adherence: " + str(Mask_Adh) + "%"  # Update mask adherence label
        parameters.update({"Mask Adherence": Mask_Adh})  # Update mask adherence within parameters

    def update_lbl_SD(Soc_Dist):
        """Update the Social Distancing label"""
        Soc_Dist = int(float((Soc_Dist)))  # Convert from Tkinter IntVar() to Int
        SD_label['text'] = "Social distancing adherence: " + str(Soc_Dist) + "%"  # Update social distancing label
        parameters.update({"Social Distancing Adherence": Soc_Dist})  # Update social distancing within parameters

    def update_lbl_SimDur(Sim_Dur):
        """Update the Simulation Duration label"""
        Sim_Dur = int(float((Sim_Dur)))  # Convert from Tkinter IntVar() to Int
        Sim_Dur_label['text'] = "Simulation duration: " + str(
            Sim_Dur) + " iterations"  # Update simulation duration label
        parameters.update({"Simulation Duration": Sim_Dur})  # Update simulation duration within parameters

    def update_lb_office_plans():
        """Update the Office Plans selection and check that the number of people and number of infected are valid for
        that office.If there are too many people then reset the select box value to the number desks (maximum allowed
        for that office)"""
        office_plans_var = Office_Plans_Listbox.curselection()  # Fetch current office floor selection
        # This is a get-around to issue where listbox lamba function is called on both selection and deselection - in
        # the case where nothing is selected "()" we do not  want the value of office plan to be reassigned
        if office_plans_var != ():
            parameters.update({"Office Plan": office_plans_var[0]})  # Update office plan within parameters
            desk_no = simulation.get_desk_no(parameters)  # Get number of desks from simulation.py
            People_Val = int(Num_People.get())  # Get Number of people
            Infected_People_Val = int(Inf_People.get())  # Get Number of infected people
            # If the number of people exceeds the number of desks for that office selection set the number of people
            # to the number of desks
            if People_Val > desk_no:
                Num_People.set(desk_no)
                parameters.update({"Number of People": desk_no})
            # If the number of infected people exceeds the number of desks for that office selection set the number of
            # people to the number of desks
            if Infected_People_Val > desk_no:
                Inf_People.set(desk_no)
                parameters.update({"Number of Infected": desk_no})

            Num_People.config(to=desk_no)  # Limit max number of people based on number of desks for new office
            Inf_People.config(to=desk_no)  # Limit max number of infected based on number of desks for new office
            office = Office(parameters['Office Plan']) # Update office plan in parameters
            display_array = simulation.input2disp(office.input_array)  # Fetch new office layout
            update_plot(display_array, 0)  # Update figure in Tkinter window

    def inc_lb_num_people():
        """Increase the number of people label if applicable and check that it doesnt exceed the number of desks"""
        # If the number of people parameter is empty (can sometimes occur as an error when the GUI is initialised) then
        # set it from parameters
        if Num_People.get() == '':
            Num_People.set(parameters['Number of People'])

        People_Val = int(float(Num_People.get()))  # Get Number of people
        desk_no = simulation.get_desk_no(parameters)  # Get number of desks from simulation.py
        # If the number of people is greater than or equal to the number of desks set the number of people to the number
        # of desks (This is only required when the Office Plan is changed)

        if People_Val >= desk_no:
            Num_People.set(desk_no)
        # If the number of people is less than the the number of desks increase the number of people
        if People_Val < desk_no:
            People_Val = People_Val + 1

        parameters.update({"Number of People": int(People_Val)})  # Update the number of people in parameters
        Inf_People.config(to=People_Val)  # Set the maximum value of the 'number of infected' slider

    def dec_lb_num_people():
        """Decrease the number of people label if applicable and check that it doesnt result in the number of infected
        exceeding the number of people"""
        # If the number of people parameter is empty (can sometimes occur as an error when the GUI is initialised)
        # then set it from parameters
        if Num_People.get() == '':
            Num_People.set(parameters['Number of People'])

        People_Val = int(float(Num_People.get()))  # Get Number of people
        Infected_People_Val = int(Inf_People.get())  # Get Number of infected people
        # Decrease the number of people as long as it wouldn't result in the number of infected exceeding the number of
        # people
        if People_Val != Infected_People_Val:
            People_Val = People_Val - 1
        parameters.update({"Number of People": People_Val})  # Update the number of people in parameters
        Inf_People.config(to=People_Val)  # Set the maximum value of the 'number of infected' spinbox

    def update_plot(frame, timestamp):
        """Update the GUI office plot"""
        infected_no = np.count_nonzero(frame == 177)
        people_no = infected_no + np.count_nonzero(frame == 22)
        test_plot = Figure(figsize=(6, 7), dpi=100, )
        new_plot = test_plot.add_subplot()
        new_plot.imshow(frame)
        new_plot.axis('off')
        if timestamp > 0:
            new_plot.title.set_text('Time: ' + str(timestamp)
                                    + '          Number of Infected: '
                                    + str(infected_no)
                                    + '/' + str(people_no))
            # new_plot.set_xlabel('Number of Infected: ' + str(infected_no))

        # Create a new canvas which the updated frame is plotted onto
        newcanvas = FigureCanvasTkAgg(test_plot, master=figframe)
        newcanvas.get_tk_widget().grid(column=1, row=0, sticky='we')
        newcanvas.draw_idle()
        figframe.update()

    def inc_lb_Inf_People():
        """Increase the number of infected label if applicable and check that it doesnt exceed the number of people or
        the number of desks"""
        # If the number of people parameter is empty (can sometimes occur as an error when the GUI is initialised) then
        # set it from parameters
        if Inf_People.get() == '':
            Inf_People.set(parameters['Number of Infected'])

        desk_no = simulation.get_desk_no(parameters)  # Get number of desks from simulation.py
        People_Val = int(float(Num_People.get()))  # Get Number of people
        Infected_People_Val = int(float(Inf_People.get()))  # Get Number of infected people
        # Increase the number of infected people as long as it wouldn't exceed the number of desks
        if Infected_People_Val <= desk_no:
            Infected_People_Val + 1

        # Increase the number of infected people as long as it wouldn't exceed the number of people
        if Infected_People_Val < People_Val:
            Infected_People_Val = Infected_People_Val + 1
        parameters.update({"Number of Infected": Infected_People_Val})
        Num_People.config(from_=Infected_People_Val)

    def dec_lb_Inf_People():
        """Decrease the number of infected label if applicable"""
        # If the number of infected parameter is empty (can sometimes occur as an error when the GUI is initialised)
        # then set it from parameters
        if Inf_People.get() == '':
            Inf_People.set(parameters['Number of Infected'])
        Infected_People_Val = int(float(Inf_People.get()))  # Fetch Number of infected people
        if Infected_People_Val > 1:
            Infected_People_Val = Infected_People_Val - 1  # Decrease the number of infected people
        parameters.update({"Number of Infected": Infected_People_Val})  # Update the number of infected in parameters
        Num_People.config(from_=Infected_People_Val)  # Set the minimum value of the 'number of people' spinbox

    def update_lbl_V(Virality):
        """Update virality  label"""
        Virality = int(float((Virality)))
        V_label['text'] = "Virality: " + str(Virality) + "%"  # Update virality label
        parameters.update({"Virality": Virality})  # Update virality in parameters

    def switch_on_Begin_sim_button_state():
        """Switch on the begin button state (such that it can be pressed)"""
        Begin_sim_button.state(['!disabled'])

    def switch_off_Begin_sim_button_state():
        """Switch off the begin button state (such that it cannot be pressed)"""
        if Begin_sim_button.instate(['!disabled']):
            Begin_sim_button.state(['disabled'])
        else:
            Begin_sim_button.state(['disabled'])

    def Begin_Sim():
        """Begin the simulation upon button press """
        Begin_sim_button.state(['disabled'])  # Disable the begin simulation button
        Save_sim_button.state(['disabled'])  # Disable the save simulation button
        display_frames = simulation.main(parameters)
        with open('frames.p', "wb") as f:
            pickle.dump(display_frames, f)
        timestamp = 1

        for frame in display_frames:
            update_plot(frame, timestamp)
            time.sleep(1 / 30)
            timestamp += 1

        Save_sim_button.state(['!disabled'])  # Reenable the save simulation button
        Begin_sim_button.state(['!disabled']) # Reenable the begin simulation button

    def save_sim():
        """Save the simulation as a GIF upon button press"""
        Begin_sim_button.state(['disabled'])
        Save_sim_button.state(['disabled'])
        with open('frames.p', "rb") as f:
            display_frames = pickle.load(f)
        simulation.save_outputs(display_frames)
        Begin_sim_button.state(['!disabled'])
        Save_sim_button.state(['!disabled'])

    def quit_sim():
        """Quit the GUI upon button press"""
        if os.path.exists('frames.p'):
            os.remove('frames.p')
        root.quit()

    ### (2) Initialising the parameters dictionary
    parameters = {'Maximum Age': 65,
                  'Minimum Age': 20,
                  'Mask Adherence': 75,
                  'Social Distancing Adherence': 75,
                  'Office Plan': 0,
                  'Virality': 30,
                  'Number of People': 15,
                  'Number of Infected': 2,
                  'Simulation Duration': 100}

    # (2) Setup of the GUI window, frames and figure and toolbar.
    # Main frame setup - GUI Controls
    root = Tk()
    root.title("COVID-19 MODELLING PARAMETERS")  # Set frame title
    mainframe = ttk.Frame(root, padding="2 2 12 12")  # create mainframe to house GUI controls
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))  # Position frame in window
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Second frame setup - Figure window
    figframe = ttk.Frame(root, padding="2 2 12 12")  # Create frame to display figure
    figframe.grid(column=1, row=0, sticky=(N, W, E, S))  # Position frame in window

    # Setup figure withing canvas to plot onto
    figure_plot = Figure(figsize=(6, 7), dpi=100, )  # Create figure to plot onto
    office_plot = figure_plot.add_subplot()  # Add subplot
    office = Office(parameters['Office Plan'])  # Get the initial office layout from parameters
    display_array = simulation.input2disp(office.input_array)  # Convert office plan into RGB matrix
    office_plot.imshow(display_array)  # Show office plan
    office_plot.axis('off')  # Remove axis
    canvas = FigureCanvasTkAgg(figure_plot, master=figframe)  # Create new canvas to plot onto
    canvas.get_tk_widget().grid(column=1, row=0, sticky='we')  # Position canvas in figure frame
    canvas.draw()  # Plot figure onto canvas
    figframe.update()
    root.iconbitmap('icon.ico')
    # Toolbar to manipulate figure
    toolbar = NavigationToolbar2Tk(canvas, figframe,
                                   pack_toolbar=False)  # pack_toolbar=False required for layout management
    toolbar.update()  # Toolbar automatically updates (this is a built-in function)
    toolbar.grid(column=1, row=1, sticky='we') # Position toolbar in figure frame
    canvas.mpl_connect(
        "key_press_event",
        lambda event: print(f"you pressed {event.key}"))  # popups that show when you hover over a toolbar button
    canvas.mpl_connect("key_press_event", key_press_handler)

    # (4) Setup of labels

    # Instructions label
    instructions_label = ttk.Label(mainframe, text='Please enter the following parameters:').grid(column=0, row=0,
                                                                                                  sticky='we')

    # People label
    People_label = ttk.Label(mainframe, text='Number of people:').grid(column=0, row=1, sticky='we')


    ## Infected People label
    Infected_label = ttk.Label(mainframe, text='Number of Infected people:').grid(column=0, row=3, sticky='we')

    # Max age label
    Max_Age_label = ttk.Label(mainframe)
    Max_Age_label.grid(column=0, row=5, sticky='we')

    # Min age label
    Min_Age_label = ttk.Label(mainframe)
    Min_Age_label.grid(column=0, row=7, sticky='we')

    # Mask adherence label
    Mask_Adh = IntVar()
    MA_label = ttk.Label(mainframe)
    MA_label.grid(column=0, row=9, sticky='we')

    # Social distancing label
    Soc_Dist = IntVar()
    SD_label = ttk.Label(mainframe)
    SD_label.grid(column=0, row=11, sticky='we')

    # Virality label
    V_label = ttk.Label(mainframe, text='Virality:')
    V_label.grid(column=0, row=13, sticky='we')

    # Office floor plans label
    Office_Plans_label = ttk.Label(mainframe, text='Office plan:').grid(column=0, row=14, sticky='we')

    # Simulation Duration label
    Sim_Dur_label = ttk.Label(mainframe)
    Sim_Dur_label.grid(column=0, row=17, sticky='we')

    # (5) Setup of widgets

    # Begin simulation button
    Begin_sim_button = ttk.Button(mainframe, text='Begin Simulation', command=Begin_Sim)
    Begin_sim_button.grid(column=0, row=19, sticky='we')

    # Save simulation button
    Save_sim_button = ttk.Button(mainframe, text='Save Animaiton', command=save_sim)
    Save_sim_button.grid(column=0, row=20, sticky='we')
    Save_sim_button.state(['disabled'])

    # Number of people spin box
    desk_no = simulation.get_desk_no(parameters)  # Get the number of desks from simulation.py
    People_Val = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the spinbox
    People_Val.set(parameters['Number of People'])  # set box to correct default value
    Num_People = ttk.Spinbox(mainframe, from_=parameters['Number of Infected'], to=desk_no, textvariable=People_Val)
    Num_People.grid(column=0, row=2, sticky=W)  # Position spinbox
    Num_People.state(['readonly'])  # Set the spinbox such that users cannot enter their own inputs as text
    # lambda used to create autonomous functions - If spin box value is changed the label will automatically be updated
    Num_People.bind("<<Increment>>", lambda e: inc_lb_num_people())
    Num_People.bind("<<Decrement>>", lambda e: dec_lb_num_people())

    # Number of people infected spin box
    Infected_People_Val = IntVar() # Setup Tkinter IntVar() value which reflects the current value in the spinbox
    Infected_People_Val.set(parameters['Number of Infected'])  # set box to correct default value
    Inf_People = ttk.Spinbox(mainframe, from_=1.0, to=parameters['Number of People'], textvariable=Infected_People_Val)
    Inf_People.grid(column=0, row=4, sticky=W)
    Inf_People.state(['readonly'])
    # lambda used to create autonomous functions - If spin box value is changed the label will automatically be updated
    Inf_People.bind("<<Increment>>", lambda e: inc_lb_Inf_People())
    Inf_People.bind("<<Decrement>>", lambda e: dec_lb_Inf_People())

    # Max age slider
    Max_Age = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the slider
    Max_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Max_Age,
                               command=update_lbl_MaxAge)  # 'command' used as a callback when slider value changes
    Max_Age_Slider.grid(column=0, row=6, sticky='we')  # Position slider
    Max_Age_Slider.set(parameters['Maximum Age'])  # Set slider to correct initial value

    # Min age slider
    Min_Age = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the slider
    Min_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Min_Age,
                               command=update_lbl_MinAge)  # 'command' used as a callback when slider value changes
    Min_Age_Slider.grid(column=0, row=8, sticky='we')  # Position slider
    Min_Age_Slider.set(parameters['Minimum Age'])  # Set slider to correct initial value

    # Mask adherence slider
    Mask_Adh_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Mask_Adh,
                                command=update_lbl_MA)  # 'command' used as a callback when slider value changes
    Mask_Adh_Slider.grid(column=0, row=10, sticky='we')  # Position slider
    Mask_Adh_Slider.set(parameters['Mask Adherence'])  # Set slider to correct initial value

    # Social distancing slider
    Soc_Dist_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Soc_Dist,
                                command=update_lbl_SD)  # 'command' used as a callback when slider value changes
    Soc_Dist_Slider.grid(column=0, row=12, sticky='we')  # Position slider
    Soc_Dist_Slider.set(parameters['Social Distancing Adherence'])  # Set slider to correct initial value

    # Virality slider
    Viral = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the slider
    Viral_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Viral,
                             command=update_lbl_V)  # 'command' used as a callback when slider value changes
    Viral_Slider.grid(column=0, row=14, sticky='we')  # Position slider
    Viral_Slider.set(parameters['Virality'])  # Set slider to correct initial value

    # Office plan listbox
    Office_Plans = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]
    office_plans_var = StringVar(value=Office_Plans)  # Setup Tkinter StringVar() value
    Office_Plans_Listbox = Listbox(mainframe, listvariable=office_plans_var, height=4)  # Create listbox
    Office_Plans_Listbox.grid(column=0, row=16, sticky='we')  # Position listbox
    Office_Plans_Listbox.bind("<<ListboxSelect>>", lambda e: update_lb_office_plans())  # Automatically update upon

    # Simulation Duration slider
    Sim_Dur = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the slider
    Sim_Dur_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=10.0, to=500.0, variable=Sim_Dur,
                               command=update_lbl_SimDur)  # 'command' used as a callback when slider value changes
    Sim_Dur_Slider.grid(column=0, row=18, sticky='we')  # Position listbox
    Sim_Dur_Slider.set(parameters['Simulation Duration'])  # Set slider to correct initial value

    # Quit application button
    Quit_app_button = ttk.Button(master=mainframe, text="Quit app", command=quit_sim)
    Quit_app_button.grid(column=0, row=21, sticky='we')

    # Scalling to add space around widgets
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()  # This tells tkinter to loop continuously checking for button clicks or key presses


if __name__ == "__main__":
    GUI()
