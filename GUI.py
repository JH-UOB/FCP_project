from tkinter import *
from tkinter import ttk

class GUI:

    def __init__(self, root):

        ## Frame setup
        root.title("COVID-19 MODELLING PARAMETERS")
        mainframe = ttk.Frame(root, padding="2 2 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ##Initalisiing parameters
        parameters = {'Maximum Age': 65,
                      'Minimum Age': 18,
                      'Mask Adherence': 0.8,
                      'Social Distancing Adherence': 0.5,
                      'Office Plan': 0.5,
                      'Number of People': 15,
                      'Simulation Duration': 100}

        ## Label update functions
        def update_lbl_MaxAge(Max_Age):
            Max_Age = int(float((Max_Age)))
            Max_Age_label['text'] = "Maximum age: " + str(Max_Age) + " years old"
            parameters.update({"Maximum Age": Max_Age})

        def update_lbl_MinAge(Min_Age):
            Min_Age = int(float((Min_Age)))
            Min_Age_label['text'] = "Minimum age: " + str(Min_Age) + " years old"
            parameters.update({"Minimum Age": Min_Age})

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

        def update_lb_office_plans(office_plans_var):
            office_plans_var = Office_Plans_Listbox.curselection()
            parameters.update({"Office Plan": office_plans_var})

        def update_lb_num_people(People_Val):
            People_Val = int(Num_People.get())
            parameters.update({"Number of People": People_Val})

        def Begin_Sim():
            print(parameters)


        ### Labels and widgets

        ## Instructions label
        instructions_label = ttk.Label(mainframe, text='Please enter the following parameters:').grid(column=0, row=0, sticky=(W, E))

        ## People label
        People_label = ttk.Label(mainframe, text='Number of people:').grid(column=0, row=1, sticky=(W, E))

        ## Number of people spin box
        People_Val = IntVar()
        Num_People = ttk.Spinbox(mainframe, from_=1.0, to=20, textvariable=People_Val)
        Num_People.grid(column=0, row=2, sticky=W)
        Num_People.state(['readonly'])
        Num_People.bind("<<Increment>>", lambda e: update_lb_num_people(People_Val))
        Num_People.bind("<<Decrement>>", lambda e: update_lb_num_people(People_Val))


        ## Max age label
        Max_Age = IntVar()
        Max_Age_label = ttk.Label(mainframe)
        Max_Age_label.grid(column=0, row=3, sticky='we')

        ## Max age slider
        Max_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Max_Age, command=update_lbl_MaxAge)
        Max_Age_Slider.grid(column=0, row=4, sticky='we')
        Max_Age_Slider.set(65)

        ## Min age label
        Min_Age = IntVar()
        Min_Age_label = ttk.Label(mainframe)
        Min_Age_label.grid(column=0, row=5, sticky='we')

        ## Min age slider
        Min_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Min_Age, command=update_lbl_MinAge)
        Min_Age_Slider.grid(column=0, row=6, sticky='we')
        Min_Age_Slider.set(18)

        ## Mask adherence label
        Mask_Adh = IntVar()
        MA_label = ttk.Label(mainframe)
        MA_label.grid(column=0, row=7, sticky='we')

        ## Mask adherence slider
        Mask_Adh_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Mask_Adh, command=update_lbl_MA)
        Mask_Adh_Slider.grid(column=0, row=8, sticky='we')
        Mask_Adh_Slider.set(80)

        ## Social distancing label
        Soc_Dist = IntVar()
        SD_label = ttk.Label(mainframe)
        SD_label.grid(column=0, row=9, sticky='we')

        ## Social distancing slider
        Soc_Dist_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Soc_Dist,command=update_lbl_SD)
        Soc_Dist_Slider.grid(column=0, row=10, sticky='we')
        Soc_Dist_Slider.set(50)

        ## Office floor plans label
        Office_Plans_label = ttk.Label(mainframe, text='Office plan:').grid(column=0, row=11, sticky='we')

        ## Office plan listbox
        Office_Plans = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]
        office_plans_var = StringVar(value=Office_Plans)
        Office_Plans_Listbox = Listbox(mainframe, listvariable=office_plans_var, height=4)
        Office_Plans_Listbox.grid(column=0, row=12, sticky='we')
        Office_Plans_Listbox.bind("<<ListboxSelect>>", lambda e: update_lb_office_plans(Office_Plans_Listbox.curselection()))

        ## Simulation Duration label
        Sim_Dur = IntVar()
        Sim_Dur_label = ttk.Label(mainframe)
        Sim_Dur_label.grid(column=0, row=13, sticky='we')

        ## Simulation Duration slider
        Sim_Dur_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=10.0, to=500.0, variable=Sim_Dur, command=update_lbl_SimDur)
        Sim_Dur_Slider.grid(column=0, row=14, sticky='we')
        Sim_Dur_Slider.set(100)

        ## Begin simulation button
        Begin_sim_button = ttk.Button(mainframe, text='Begin Simulation', command=Begin_Sim)
        Begin_sim_button.grid(column=0, row=15, sticky='we')

        ##scalling to add space around widgets
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

root = Tk()
GUI(root)
root.mainloop()