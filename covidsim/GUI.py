"""

GUI.py
Designed and written by James Irvin
May 2021

This script contains a function which creates a GUI that can be used to view and the office layout and control input
parameters to simulation.py.

Used by simulation.py.
"""

# External modules
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import pickle
import os
import time
from PIL import ImageTk, Image
# Directory modules
from covidsim.office import Office
import covidsim.simulation as simulation
import gc


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
            "virality" - Percentage of virality [slider]
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

    def update_lbl_max_age(max_age):
        """Update the Max Age label and check that max age exceeds min age.
        If this is not true then the begin simulation button is disabled"""
        try:
            min_age = int(float((min_age_slider.get())))  # Get the current value of min age
        except:
            # This is required as the max age slider is initialised before the min slider - this means for the first...
            # loop the min age slider doesnt exist so in this instance min age is defined from parameters.
            min_age = parameters['Minimum Age']
        max_age = int(float((max_age)))  # Convert from Tkinter IntVar() to Int
        max_age_label['text'] = "Maximum age: " + str(max_age) + " years old"  # Update max age label
        parameters.update({"Maximum Age": max_age})  # Update max age within parameters
        if min_age > max_age:
            switch_off_begin_sim_button_state()  # disable begin sim button
        else:
            switch_on_begin_sim_button_state()  # enable begin sim button

    def update_lbl_min_age(min_age):
        """Update the Min Age label and check that max age exceeds min age.
                If this is not true then the begin simulation button is disabled"""
        min_age = int(float((min_age)))  # Convert from Tkinter IntVar() to Int
        max_age = int(float((max_age_slider.get())))  # Get the current value of max age
        min_age_label['text'] = "Minimum age: " + str(min_age) + " years old"  # Update min age label
        parameters.update({"Minimum Age": min_age})  # Update min age within parameters
        if min_age > max_age:
            switch_off_begin_sim_button_state()
        else:
            switch_on_begin_sim_button_state()

    def update_lbl_ma(mask_adh):
        """Update the Mask Adherence label"""
        mask_adh = int(float((mask_adh)))  # Convert from Tkinter IntVar() to Int
        ma_label['text'] = "Mask adherence: " + str(mask_adh) + "%"  # Update mask adherence label
        parameters.update({"Mask Adherence": mask_adh})  # Update mask adherence within parameters

    def update_lbl_sd(soc_dist):
        """Update the Social Distancing label"""
        soc_dist = int(float((soc_dist)))  # Convert from Tkinter IntVar() to Int
        sd_label['text'] = "Social distancing adherence: " + str(soc_dist) + "%"  # Update social distancing label
        parameters.update({"Social Distancing Adherence": soc_dist})  # Update social distancing within parameters

    def update_lbl_sim_dur(sim_dur):
        """Update the Simulation Duration label"""
        sim_dur = int(float((sim_dur)))  # Convert from Tkinter IntVar() to Int
        sim_dur_label['text'] = "Simulation duration: " + str(
            sim_dur) + " iterations"  # Update simulation duration label
        parameters.update({"Simulation Duration": sim_dur})  # Update simulation duration within parameters

    def update_lb_office_plans():
        """Update the Office Plans selection and check that the number of people and number of infected are valid for
        that office.If there are too many people then reset the select box value to the number desks (maximum allowed
        for that office)"""
        office_plans_var = office_plans_listbox.curselection()  # Fetch current office floor selection
        # This is a get-around to issue where listbox lamba function is called on both selection and deselection - in
        # the case where nothing is selected "()" we do not  want the value of office plan to be reassigned
        if office_plans_var != ():
            parameters.update({"Office Plan": office_plans_var[0]})  # Update office plan within parameters
            desk_no = simulation.get_desk_no(parameters)  # Get number of desks from simulation.py
            people_val = int(num_people.get())  # Get Number of people
            infected_people_val = int(inf_people.get())  # Get Number of infected people
            # If the number of people exceeds the number of desks for that office selection set the number of people
            # to the number of desks
            if people_val > desk_no:
                num_people.set(desk_no)
                parameters.update({"Number of People": desk_no})
            # If the number of infected people exceeds the number of desks for that office selection set the number of
            # people to the number of desks
            if infected_people_val > desk_no:
                inf_people.set(desk_no)
                parameters.update({"Number of Infected": desk_no})

            num_people.config(to=desk_no)  # Limit max number of people based on number of desks for new office
            inf_people.config(to=num_people.get())  # Limit max number of infected based on number of people
            office = Office(parameters['Office Plan']) # Update office plan in parameters
            display_array = simulation.input2disp(office.input_array)  # Fetch new office layout
            update_plot(display_array, 0)  # Update figure in Tkinter window

    def inc_lb_num_people():
        """Increase the number of people label if applicable and check that it doesnt exceed the number of desks"""
        # If the number of people parameter is empty (can sometimes occur as an error when the GUI is initialised) then
        # set it from parameters
        if num_people.get() == '':
            num_people.set(parameters['Number of People'])

        people_val = int(float(num_people.get()))  # Get Number of people
        desk_no = simulation.get_desk_no(parameters)  # Get number of desks from simulation.py
        # If the number of people is greater than or equal to the number of desks set the number of people to the number
        # of desks (This is only required when the Office Plan is changed)

        if people_val >= desk_no:
            num_people.set(desk_no)
        # If the number of people is less than the the number of desks increase the number of people
        if people_val < desk_no:
            people_val = people_val + 1

        parameters.update({"Number of People": int(people_val)})  # Update the number of people in parameters
        inf_people.config(to=people_val)  # Set the maximum value of the 'number of infected' slider

    def dec_lb_num_people():
        """Decrease the number of people label if applicable and check that it doesnt result in the number of infected
        exceeding the number of people"""
        # If the number of people parameter is empty (can sometimes occur as an error when the GUI is initialised)
        # then set it from parameters
        if num_people.get() == '':
            num_people.set(parameters['Number of People'])

        people_val = int(float(num_people.get()))  # Get Number of people
        infected_people_val = int(inf_people.get())  # Get Number of infected people
        # Decrease the number of people as long as it wouldn't result in the number of infected exceeding the number of
        # people
        if people_val != infected_people_val:
            people_val = people_val - 1
        parameters.update({"Number of People": people_val})  # Update the number of people in parameters
        inf_people.config(to=people_val)  # Set the maximum value of the 'number of infected' spinbox

    def update_plot(frame, timestamp):
        """Update the GUI office plot"""
        # Get number of people who are infected or contagious based on number of
        # array cells in red and orange
        infected_no = np.count_nonzero(frame == 177) + np.count_nonzero(frame == 237)
        # Add number of healthy people to infected and contagious people to get
        # total population.
        # This is necessary as the simulation only outputs display frames without
        # explicit infection data
        people_no = infected_no + np.count_nonzero(frame == 22)
        # Create infection plot from display frame
        test_plot = Figure(figsize=(6, 7), dpi=100, )
        new_plot = test_plot.add_subplot()
        new_plot.imshow(frame)
        new_plot.axis('off')
        new_plot.title.set_text('Time: ' + str(timestamp)
                                    + '          Number of Infected: '
                                    + str(infected_no)
                                    + '/' + str(people_no))

        # Create a new canvas which the updated frame is plotted onto
        newcanvas = FigureCanvasTkAgg(test_plot, master=figframe)
        newcanvas.get_tk_widget().grid(column=0, row=1, sticky='we')
        newcanvas.draw_idle()
        figframe.update()

    def inc_lb_inf_people():
        """Increase the number of infected label if applicable and check that it doesnt exceed the number of people or
        the number of desks"""
        # If the number of people parameter is empty (can sometimes occur as an error when the GUI is initialised) then
        # set it from parameters
        if inf_people.get() == '':
            inf_people.set(parameters['Number of Infected'])

        desk_no = simulation.get_desk_no(parameters)  # Get number of desks from simulation.py
        people_val = int(float(num_people.get()))  # Get Number of people
        infected_people_val = int(float(inf_people.get()))  # Get Number of infected people
        # Increase the number of infected people as long as it wouldn't exceed the number of desks

        # Increase the number of infected people as long as it wouldn't exceed the number of people
        if infected_people_val < people_val:
            infected_people_val = infected_people_val + 1
        parameters.update({"Number of Infected": infected_people_val})
        num_people.config(from_=infected_people_val)

    def dec_lb_inf_people():
        """Decrease the number of infected label if applicable"""
        # If the number of infected parameter is empty (can sometimes occur as an error when the GUI is initialised)
        # then set it from parameters
        if inf_people.get() == '':
            inf_people.set(parameters['Number of Infected'])
        infected_people_val = int(float(inf_people.get()))  # Fetch Number of infected people
        if infected_people_val > 1:
            infected_people_val = infected_people_val - 1  # Decrease the number of infected people
        parameters.update({"Number of Infected": infected_people_val})  # Update the number of infected in parameters
        num_people.config(from_=infected_people_val)  # Set the minimum value of the 'number of people' spinbox

    def update_lbl_v(virality):
        """Update virality  label"""
        virality = int(float((virality)))
        v_label['text'] = "Virality: " + str(virality) + "%"  # Update virality label
        parameters.update({"Virality": virality})  # Update virality in parameters

    def switch_on_begin_sim_button_state():
        """Switch on the begin button state (such that it can be pressed)"""
        begin_sim_button.state(['!disabled'])

    def switch_off_begin_sim_button_state():
        """Switch off the begin button state (such that it cannot be pressed)"""
        if begin_sim_button.instate(['!disabled']):
            begin_sim_button.state(['disabled'])
        else:
            begin_sim_button.state(['disabled'])

    def begin_sim():
        """Begin the simulation upon button press """
        gc.collect()  # remove previous simulations from RAM     
        begin_sim_button.state(['disabled'])  # Disable the save simulation button
        save_sim_button.state(['disabled'])  # Disable the save simulation button
        replay_animation_button.state(['disabled'])  # Disable the save simulation button
        display_frames = simulation.main(parameters)
        with open('./gui_files/frames.p', "wb") as f:
            pickle.dump(display_frames, f)
        timestamp = 1

        for frame in display_frames:
            update_plot(frame, timestamp)
            time.sleep(1 / 30)
            timestamp += 1

        save_sim_button.state(['!disabled'])  # Reenable the save simulation button
        replay_animation_button.state(['!disabled'])  # Reenable the save simulation button
        begin_sim_button.state(['!disabled']) # Reenable the begin simulation button

    def replay_animation():
        """Replay animation of simulation that has just been run"""
        begin_sim_button.state(['disabled'])  # Disable the begin simulation button
        save_sim_button.state(['disabled'])  # Disable the save simulation button
        replay_animation_button.state(['disabled'])  # Reenable the save simulation button
        # Load in frames
        with open('./gui_files/frames.p', "rb") as f:
            display_frames = pickle.load(f)
        timestamp = 1
        # Display frames
        for frame in display_frames:
            update_plot(frame, timestamp)
            time.sleep(1 / 30)
            timestamp += 1

        save_sim_button.state(['!disabled'])  # Reenable the save simulation button
        replay_animation_button.state(['!disabled'])  # Reenable the save simulation button
        begin_sim_button.state(['!disabled']) # Reenable the begin simulation button


    def save_sim():
        """Save the simulation as a GIF upon button press"""
        begin_sim_button.state(['disabled'])  # Disable the begin simulation button
        save_sim_button.state(['disabled'])  # Disable the save simulation button
        replay_animation_button.state(['disabled'])  # Reenable the save simulation button
        # Load in frames
        with open('./gui_files/frames.p', "rb") as f:
            display_frames = pickle.load(f)
        # Save frames
        simulation.save_outputs(display_frames)
        save_sim_button.state(['!disabled'])  # Reenable the save simulation button
        replay_animation_button.state(['!disabled'])  # Reenable the save simulation button
        begin_sim_button.state(['!disabled']) # Reenable the begin simulation button

    def quit_sim():
        """Quit the GUI upon button press"""
        if os.path.exists('./gui_files/frames.p'):
            os.remove('./gui_files/frames.p')
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

    # Add key
    img = Image.open('./gui_files/plot_key.png').resize((440, 40), Image.ANTIALIAS)  # Get key image and resize
    key = ImageTk.PhotoImage(img)  # Add image to tkinter
    key_plot = Label(figframe, image=key)  # plot image
    key_plot.grid(column=0, row=0, sticky='we')  # position key in frame

    # Setup office figure withing canvas to plot onto
    figure_plot = Figure(figsize=(6, 7), dpi=100)  # Create figure to plot onto
    office_plot = figure_plot.add_subplot()  # Add subplot
    office = Office(parameters['Office Plan'])  # Get the initial office layout from parameters
    display_array = simulation.input2disp(office.input_array)  # Convert office plan into RGB matrix
    office_plot.imshow(display_array)  # Show office plan
    office_plot.axis('off')  # Remove axis
    canvas = FigureCanvasTkAgg(figure_plot, master=figframe)  # Create new canvas to plot onto
    canvas.get_tk_widget().grid(column=0, row=1, sticky='we')  # Position canvas in figure frame
    canvas.draw()  # Plot figure onto canvas
    figframe.update()
    root.iconbitmap('./gui_files/icon.ico')
    # Toolbar to manipulate figure
    toolbar = NavigationToolbar2Tk(canvas, figframe,
                                   pack_toolbar=False)  # pack_toolbar=False required for layout management
    toolbar.update()  # Toolbar automatically updates (this is a built-in function)
    toolbar.grid(column=0, row=2, sticky='we') # Position toolbar in figure frame
    canvas.mpl_connect(
        "key_press_event",
        lambda event: print(f"you pressed {event.key}"))  # popups that show when you hover over a toolbar button
    canvas.mpl_connect("key_press_event", key_press_handler)

    # (4) Setup of labels

    # Instructions label
    instructions_label = ttk.Label(mainframe, text='Please enter the following parameters:').grid(column=0, row=0,
                                                                                                  sticky='we')

    # People label
    people_label = ttk.Label(mainframe, text='Number of people:').grid(column=0, row=1, sticky='we')


    ## Infected People label
    infected_label = ttk.Label(mainframe, text='Number of Infected people:').grid(column=0, row=3, sticky='we')

    # Max age label
    max_age_label = ttk.Label(mainframe)
    max_age_label.grid(column=0, row=5, sticky='we')

    # Min age label
    min_age_label = ttk.Label(mainframe)
    min_age_label.grid(column=0, row=7, sticky='we')

    # Mask adherence label
    mask_adh = IntVar()
    ma_label = ttk.Label(mainframe)
    ma_label.grid(column=0, row=9, sticky='we')

    # Social distancing label
    soc_dist = IntVar()
    sd_label = ttk.Label(mainframe)
    sd_label.grid(column=0, row=11, sticky='we')

    # virality label
    v_label = ttk.Label(mainframe, text='Virality:')
    v_label.grid(column=0, row=13, sticky='we')

    # Office floor plans label
    office_plans_label = ttk.Label(mainframe, text='Office plan:').grid(column=0, row=14, sticky='we')

    # Simulation Duration label
    sim_dur_label = ttk.Label(mainframe)
    sim_dur_label.grid(column=0, row=17, sticky='we')


    # (5) Setup of widgets

    # Begin simulation button
    begin_sim_button = ttk.Button(mainframe, text='Begin Simulation', command=begin_sim)
    begin_sim_button.grid(column=0, row=19, sticky='we')

    # Save simulation button
    save_sim_button = ttk.Button(mainframe, text='Save Animaiton', command=save_sim)
    save_sim_button.grid(column=0, row=21, sticky='we')
    save_sim_button.state(['disabled'])

    # Number of people spin box
    desk_no = simulation.get_desk_no(parameters)  # Get the number of desks from simulation.py
    people_val = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the spinbox
    people_val.set(parameters['Number of People'])  # set box to correct default value
    num_people = ttk.Spinbox(mainframe, from_=parameters['Number of Infected'], to=desk_no, textvariable=people_val)
    num_people.grid(column=0, row=2, sticky=W)  # Position spinbox
    num_people.state(['readonly'])  # Set the spinbox such that users cannot enter their own inputs as text
    # lambda used to create autonomous functions - If spin box value is changed the label will automatically be updated
    num_people.bind("<<Increment>>", lambda e: inc_lb_num_people())
    num_people.bind("<<Decrement>>", lambda e: dec_lb_num_people())

    # Number of people infected spin box
    infected_people_val = IntVar() # Setup Tkinter IntVar() value which reflects the current value in the spinbox
    infected_people_val.set(parameters['Number of Infected'])  # set box to correct default value
    inf_people = ttk.Spinbox(mainframe, from_=1.0, to=parameters['Number of People'], textvariable=infected_people_val)
    inf_people.grid(column=0, row=4, sticky=W)
    inf_people.state(['readonly'])
    # lambda used to create autonomous functions - If spin box value is changed the label will automatically be updated
    inf_people.bind("<<Increment>>", lambda e: inc_lb_inf_people())
    inf_people.bind("<<Decrement>>", lambda e: dec_lb_inf_people())

    # Max age slider
    max_age = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the slider
    max_age_slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=max_age,
                               command=update_lbl_max_age)  # 'command' used as a callback when slider value changes
    max_age_slider.grid(column=0, row=6, sticky='we')  # Position slider
    max_age_slider.set(parameters['Maximum Age'])  # Set slider to correct initial value

    # Min age slider
    min_age = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the slider
    min_age_slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=min_age,
                               command=update_lbl_min_age)  # 'command' used as a callback when slider value changes
    min_age_slider.grid(column=0, row=8, sticky='we')  # Position slider
    min_age_slider.set(parameters['Minimum Age'])  # Set slider to correct initial value

    # Mask adherence slider
    mask_adh_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=mask_adh,
                                command=update_lbl_ma)  # 'command' used as a callback when slider value changes
    mask_adh_Slider.grid(column=0, row=10, sticky='we')  # Position slider
    mask_adh_Slider.set(parameters['Mask Adherence'])  # Set slider to correct initial value

    # Social distancing slider
    soc_dist_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=soc_dist,
                                command=update_lbl_sd)  # 'command' used as a callback when slider value changes
    soc_dist_Slider.grid(column=0, row=12, sticky='we')  # Position slider
    soc_dist_Slider.set(parameters['Social Distancing Adherence'])  # Set slider to correct initial value

    # virality slider
    viral = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the slider
    viral_slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=viral,
                             command=update_lbl_v)  # 'command' used as a callback when slider value changes
    viral_slider.grid(column=0, row=14, sticky='we')  # Position slider
    viral_slider.set(parameters['Virality'])  # Set slider to correct initial value

    # Office plan listbox
    office_plans = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]
    office_plans_var = StringVar(value=office_plans)  # Setup Tkinter StringVar() value
    office_plans_listbox = Listbox(mainframe, listvariable=office_plans_var, height=4)  # Create listbox
    office_plans_listbox.grid(column=0, row=16, sticky='we')  # Position listbox
    office_plans_listbox.bind("<<ListboxSelect>>", lambda e: update_lb_office_plans())  # Automatically update upon

    # Simulation Duration slider
    sim_dur = IntVar()  # Setup Tkinter IntVar() value which reflects the current value in the slider
    sim_dur_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=10.0, to=500.0, variable=sim_dur,
                               command=update_lbl_sim_dur)  # 'command' used as a callback when slider value changes
    sim_dur_Slider.grid(column=0, row=18, sticky='we')  # Position listbox
    sim_dur_Slider.set(parameters['Simulation Duration'])  # Set slider to correct initial value

    # Replay animation button
    replay_animation_button = ttk.Button(master=mainframe, text="Replay Animaiton", command=replay_animation)
    replay_animation_button.grid(column=0, row=20, sticky='we')
    replay_animation_button.state(['disabled'])

    # Quit application button
    quit_app_button = ttk.Button(master=mainframe, text="Quit App", command=quit_sim)
    quit_app_button.grid(column=0, row=22, sticky='we')

    # Scalling to add space around widgets
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)
    for child in figframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()  # This tells tkinter to loop continuously checking for button clicks or key presses


if __name__ == "__main__":
    GUI()
