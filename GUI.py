"""

GUI.py
Designed and written by James Irvin
May 2021

This script contains a class that defines the GUI and plots the outputs of simulation.py as an animated office.

Used by simulation.py.
"""

## Import modules
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
def main():
    ### (3) Functions which handle callbacks

    def update_lbl_MaxAge(Max_Age):
        try:
            Min_Age = int(float((Min_Age_Slider.get())))
        except:
            Min_Age = parameters['Minimum Age']

        Max_Age = int(float((Max_Age)))
        Max_Age_label['text'] = "Maximum age: " + str(Max_Age) + " years old"
        parameters.update({"Maximum Age": Max_Age})
        if Min_Age > Max_Age:
            switch_off_Begin_sim_button_state()
        else:
            switch_on_Begin_sim_button_state()

    def update_lbl_MinAge(Min_Age):
        Min_Age = int(float((Min_Age)))
        Max_Age = int(float((Max_Age_Slider.get())))
        Min_Age_label['text'] = "Minimum age: " + str(Min_Age) + " years old"
        parameters.update({"Minimum Age": Min_Age})
        if Min_Age > Max_Age:
            switch_off_Begin_sim_button_state()
        else:
            switch_on_Begin_sim_button_state()

    def update_lbl_MA(Mask_Adh):
        Mask_Adh = int(float((Mask_Adh)))
        MA_label['text'] = "Mask adherence: " + str(Mask_Adh) + "%"
        parameters.update({"Mask Adherence": Mask_Adh})

    def update_lbl_SD(Soc_Dist):
        Soc_Dist = int(float((Soc_Dist)))
        SD_label['text'] = "Social distancing adherence: " + str(Soc_Dist) + "%"
        parameters.update({"Social Distancing Adherence": Soc_Dist})

    def update_lbl_SimDur(Sim_Dur):
        Sim_Dur = int(float((Sim_Dur)))
        Sim_Dur_label['text'] = "Simulation duration: " + str(Sim_Dur) + " iterations"
        parameters.update({"Simulation Duration": Sim_Dur})

    def update_lb_office_plans():
        office_plans_var = Office_Plans_Listbox.curselection()
        if office_plans_var != ():  # This is a get-around to issue where listbox lamba function is called on both selection and deselection - In the case where nothing is selected "()" we do not want the value of office plan to be reassigned
            parameters.update({"Office Plan": office_plans_var[0]})
            desk_no = simulation.get_desk_no(parameters)
            People_Val = int(Num_People.get())  # Fetch Number of people
            Infected_People_Val = int(Inf_People.get())  # Fetch Number of infected people
            if People_Val > desk_no:  # If the number of people exceeds the number of desks for that office selection set the number of people to the number of desks
                Num_People.set(desk_no)
                parameters.update({"Number of People": desk_no})
            if Infected_People_Val > desk_no:
                Inf_People.set(desk_no)
                parameters.update({"Number of infected": desk_no})
            Num_People.config(to=desk_no)  # Limit max number of people based on number of desks
            Inf_People.config(to=desk_no)
            office = Office(parameters['Office Plan'])
            display_array = simulation.input2disp(office.input_array)
            update_plot(display_array, 0)

    def inc_lb_num_people():
        if Num_People.get() == '':
            Num_People.set(parameters['Number of People'])
        People_Val = int(float(Num_People.get()))  # Fetch Number of people
        desk_no = simulation.get_desk_no(parameters)
        if People_Val >= desk_no:  # If the number of people is greater than or equal to the number of desks set the number of people to the number of desks (This is only required when the Office Plan is changed
            Num_People.set(desk_no)
        if People_Val < desk_no:  # If the number of people is less than the the number of desks increase the number of people
            People_Val = People_Val + 1
        parameters.update({"Number of People": int(People_Val)})
        Inf_People.config(to=People_Val)

    def dec_lb_num_people():
        if Num_People.get() == '':
            Num_People.set(parameters['Number of People'])
        People_Val = int(float(Num_People.get()))  # Fetch Number of people
        Infected_People_Val = int(Inf_People.get())  # Fetch Number of infected people
        if People_Val != Infected_People_Val:  # Decrease the number of people as long as it wouldnt result in the number of infected exceeding the number of people
            People_Val = People_Val - 1
        parameters.update({"Number of People": People_Val})
        Inf_People.config(to=People_Val)

    def update_plot(frame, timestamp):
        infected_no = np.count_nonzero(frame == 177)
        people_no = infected_no + np.count_nonzero(frame == 22)
        test_plot = Figure(figsize=(6, 7), dpi=100, )
        new_plot = test_plot.add_subplot()
        new_plot.imshow(frame)
        new_plot.axis('off')
        if timestamp > 0:
            new_plot.title.set_text('Time: ' + str(timestamp) 
                                    +'          Number of Infected: ' 
                                    + str(infected_no) 
                                    + '/' + str(people_no))
            # new_plot.set_xlabel('Number of Infected: ' + str(infected_no))
        newcanvas = FigureCanvasTkAgg(test_plot, master=figframe)
        newcanvas.get_tk_widget().grid(column=1, row=0, sticky='we')
        newcanvas.draw_idle()
        figframe.update()

    def inc_lb_Inf_People():
        if Inf_People.get() == '':
            Inf_People.set(parameters['Number of infected'])
        desk_no = simulation.get_desk_no(parameters)
        People_Val = int(float(Num_People.get()))  # Fetch Number of people
        Infected_People_Val = int(float(Inf_People.get()))  # Fetch Number of infected people
        if Infected_People_Val <= desk_no:
            Infected_People_Val + 1
        if Infected_People_Val < People_Val:  # Increase the number of infeceted people as long as it wouldnt exceed the number of people
            Infected_People_Val = Infected_People_Val + 1
        parameters.update({"Number of infected": Infected_People_Val})
        Num_People.config(from_=Infected_People_Val)

    def dec_lb_Inf_People():
        if Inf_People.get() == '':
            Inf_People.set(parameters['Number of infected'])

        Infected_People_Val = int(float(Inf_People.get()))  # Fetch Number of infected people
        if Infected_People_Val > 1:
            Infected_People_Val = Infected_People_Val - 1  # Decrease the number of infected people
        parameters.update({"Number of infected": Infected_People_Val})
        Num_People.config(from_=Infected_People_Val)

    def update_lbl_V(Virality):
        Virality = int(float((Virality)))
        V_label['text'] = "Virality: " + str(Virality) + "%"
        parameters.update({"Virality": Virality})

    def switch_on_Begin_sim_button_state():
        Begin_sim_button.state(['!disabled'])

    def switch_off_Begin_sim_button_state():
        if Begin_sim_button.instate(['!disabled']):
            Begin_sim_button.state(['disabled'])
        else:
            Begin_sim_button.state(['disabled'])

    def Begin_Sim():
        # print(parameters)
        Begin_sim_button.state(['disabled'])
        Save_sim_button.state(['disabled'])
        display_frames = simulation.main(parameters)
        with open('frames.p', "wb") as f:
            pickle.dump(display_frames, f)
        timestamp = 1
        for frame in display_frames:
            update_plot(frame, timestamp)
            time.sleep(1 / 30)
            timestamp += 1
        Save_sim_button.state(['!disabled'])
        Begin_sim_button.state(['!disabled'])

    def save_sim():
        Begin_sim_button.state(['disabled'])
        Save_sim_button.state(['disabled'])
        with open('frames.p', "rb") as f:
            display_frames = pickle.load(f)
        simulation.save_outputs(display_frames)
        Begin_sim_button.state(['!disabled'])
        Save_sim_button.state(['!disabled'])

    def quit_sim():
        if os.path.exists('frames.p'):
            os.remove('frames.p')
        root.quit()

    root = Tk()

    ### (1) Initialising the parameters dictionary
    parameters = {'Maximum Age': 65,
                  'Minimum Age': 20,
                  'Mask Adherence': 80,
                  'Social Distancing Adherence': 50,
                  'Office Plan': 0,
                  'Virality': 50,
                  'Number of People': 15,
                  'Number of infected': 5,
                  'Simulation Duration': 12}

    ### (2) Setup of the GUI window, frames and figure and toolbar.
    ## Main frame setup - GUI Controls
    root.title("COVID-19 MODELLING PARAMETERS")
    mainframe = ttk.Frame(root, padding="2 2 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ## Second frame setup - Figure window
    figframe = ttk.Frame(root, padding="2 2 12 12")
    figframe.grid(column=1, row=0, sticky=(N, W, E, S))


    ## Setup figure withing canvas to plot onto
    figure_plot = Figure(figsize=(6, 7), dpi=100, )
    y = np.random.random([10, 1])
    office_plot = figure_plot.add_subplot()
    office = Office(parameters['Office Plan'])
    display_array = simulation.input2disp(office.input_array)
    office_plot.imshow(display_array)
    office_plot.axis('off')
    canvas = FigureCanvasTkAgg(figure_plot, master=figframe)
    canvas.get_tk_widget().grid(column=1, row=0, sticky='we')
    canvas.draw()
    figframe.update()
    root.iconbitmap('icon.ico')
    ## Toolbar to manipulate figure
    toolbar = NavigationToolbar2Tk(canvas, figframe, pack_toolbar=False) # pack_toolbar=False required for layout managment.
    toolbar.update() # Toolbar automatically updates (this is a built in function)
    toolbar.grid(column=1, row=1, sticky='we')
    canvas.mpl_connect(
        "key_press_event", lambda event: print(f"you pressed {event.key}")) # popups that show when you hover over a toolbar button
    canvas.mpl_connect("key_press_event", key_press_handler)

    ### (4) Setup of labels

    ## Instructions label
    instructions_label = ttk.Label(mainframe, text='Please enter the following parameters:').grid(column=0, row=0, sticky='we')

    ## People label
    People_label = ttk.Label(mainframe, text='Number of people:').grid(column=0, row=1, sticky='we')

    ## Infected People label
    Infected_label= ttk.Label(mainframe, text='Number of infected people:').grid(column=0, row=3, sticky='we')

    ## Max age label
    Max_Age_label = ttk.Label(mainframe)
    Max_Age_label.grid(column=0, row=5, sticky='we')

    ## Min age label
    Min_Age_label = ttk.Label(mainframe)
    Min_Age_label.grid(column=0, row=7, sticky='we')

    ## Mask adherence label
    Mask_Adh = IntVar()
    MA_label = ttk.Label(mainframe)
    MA_label.grid(column=0, row=9, sticky='we')

    ## Social distancing label
    Soc_Dist = IntVar()
    SD_label = ttk.Label(mainframe)
    SD_label.grid(column=0, row=11, sticky='we')

    ## Virality label
    V_label = ttk.Label(mainframe,text='Virality:')
    V_label.grid(column=0, row=13, sticky='we')

    ## Office floor plans label
    Office_Plans_label = ttk.Label(mainframe, text='Office plan:').grid(column=0, row=14, sticky='we')

    ## Simulation Duration label
    Sim_Dur_label = ttk.Label(mainframe)
    Sim_Dur_label.grid(column=0, row=17, sticky='we')

    ### (5) Setup of widgets

    ## Begin simulation button
    Begin_sim_button = ttk.Button(mainframe, text='Begin Simulation', command=Begin_Sim)
    Begin_sim_button.grid(column=0, row=19, sticky='we')

    ## Save simulation button
    Save_sim_button = ttk.Button(mainframe, text='Save Animaiton', command=save_sim)
    Save_sim_button.grid(column=0, row=20, sticky='we')
    Save_sim_button.state(['disabled'])

    ## Number of people spin box
    # office = Office(parameters['Office Plan'][0]) # Fetch the office plan parameters
    # desk_no = len(office.desk_locations) # Calculate the number of desks to set the maximum number of people
    desk_no = simulation.get_desk_no(parameters)
    People_Val = IntVar()
    People_Val.set(parameters['Number of People'])  # set box to correct default value
    Num_People = ttk.Spinbox(mainframe,from_ =parameters['Number of infected'], to=desk_no, textvariable=People_Val)
    Num_People.grid(column=0, row=2, sticky=W)
    Num_People.state(['readonly'])
    Num_People.bind("<<Increment>>", lambda e: inc_lb_num_people())  # lambda used to create autonimous functions - If spin box valaue is changed the label will automatcailly be updated
    Num_People.bind("<<Decrement>>", lambda e: dec_lb_num_people())

    ## Number of people infected spin box
    Infected_People_Val = IntVar()
    Infected_People_Val.set(parameters['Number of infected'])  # set box to correct default value
    Inf_People = ttk.Spinbox(mainframe, from_=1.0, to=parameters['Number of People'], textvariable=Infected_People_Val)
    Inf_People.grid(column=0, row=4, sticky=W)
    Inf_People.state(['readonly'])
    Inf_People.bind("<<Increment>>", lambda e: inc_lb_Inf_People())
    Inf_People.bind("<<Decrement>>", lambda e: dec_lb_Inf_People())

    ## Max age slider
    Max_Age = IntVar()
    Max_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Max_Age, command=update_lbl_MaxAge)
    Max_Age_Slider.grid(column=0, row=6, sticky='we')
    Max_Age_Slider.set(parameters['Maximum Age'])

    ## Min age slider
    Min_Age = IntVar()
    Min_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Min_Age, command=update_lbl_MinAge)
    Min_Age_Slider.grid(column=0, row=8, sticky='we')
    Min_Age_Slider.set(parameters['Minimum Age'])

    ## Mask adherence slider
    Mask_Adh_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Mask_Adh, command=update_lbl_MA)
    Mask_Adh_Slider.grid(column=0, row=10, sticky='we')
    Mask_Adh_Slider.set(parameters['Mask Adherence'])

    ## Social distancing slider
    Soc_Dist_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Soc_Dist,command=update_lbl_SD)
    Soc_Dist_Slider.grid(column=0, row=12, sticky='we')
    Soc_Dist_Slider.set(parameters['Social Distancing Adherence'])


    ## Virality slider
    Viral = IntVar()
    Viral_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Viral,command=update_lbl_V)
    Viral_Slider.grid(column=0, row=14, sticky='we')
    Viral_Slider.set(parameters['Virality'])

    ## Office plan listbox
    Office_Plans = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]
    office_plans_var = StringVar(value=Office_Plans)
    Office_Plans_Listbox = Listbox(mainframe, listvariable=office_plans_var, height=4)
    Office_Plans_Listbox.grid(column=0, row=16, sticky='we')
    Office_Plans_Listbox.bind("<<ListboxSelect>>", lambda e: update_lb_office_plans())

    ## Simulation Duration slider
    Sim_Dur = IntVar()
    Sim_Dur_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=10.0, to=500.0, variable=Sim_Dur, command=update_lbl_SimDur)
    Sim_Dur_Slider.grid(column=0, row=18, sticky='we')
    Sim_Dur_Slider.set(parameters['Simulation Duration'])

    ## Quit application button
    Quit_app_button = ttk.Button(master=mainframe, text="Quit app", command=quit_sim)
    Quit_app_button.grid(column=0, row=21, sticky='we')

    ##scalling to add space around widgets
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
