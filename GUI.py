from tkinter import *
from tkinter import ttk


class GUI:

    def __init__(self, root):

        root.title("COVID-19 MODELLING PARAMETERS")
        mainframe = ttk.Frame(root, padding="2 2 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        instructions_label = ttk.Label(mainframe, text='Please enter the following parameters:').grid(column=0, row=0, sticky=(W, E))
        # People label
        People_label = ttk.Label(mainframe, text='Number of people:').grid(column=0, row=1, sticky=(W, E))

        ## Number of people spin box
        spinval = StringVar()
        Numpeople = ttk.Spinbox(mainframe, from_=1.0, to=20, textvariable=spinval).grid(column=0, row=2, sticky=W)

        ## Max age slider
        Max_Age = IntVar()
        Max_Age_label = ttk.Label(mainframe)
        Max_Age_label.grid(column=0, row=3, sticky='we')

        def update_lbl_MaxAge(Max_Age):
            Max_Age_label['text'] = "Maximum age: " + Max_Age + " years old"

        Max_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Max_Age,
                          command=update_lbl_MaxAge)
        Max_Age_Slider.grid(column=0, row=4, sticky='we')
        Max_Age_Slider.set(60)

        ## Min age slider
        Min_Age = IntVar()
        Min_Age_label = ttk.Label(mainframe)
        Min_Age_label.grid(column=0, row=5, sticky='we')

        def update_lbl_MinAge(Min_Age):
            Min_Age_label['text'] = "Minimum age: " + Min_Age + " years old"

        Min_Age_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=16.0, to=120.0, variable=Min_Age,
                          command=update_lbl_MinAge)
        Min_Age_Slider.grid(column=0, row=6, sticky='we')
        Min_Age_Slider.set(18)

        ## Mask Adherance slider
        Mask_Adh = IntVar()
        MA_label = ttk.Label(mainframe)
        MA_label.grid(column=0, row=7, sticky='we')


        def update_lbl_MA(Mask_Adh):
            MA_label['text'] = "Mask adherence: " + Mask_Adh + "%"
        Mask_Adh_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Mask_Adh, command=update_lbl_MA)
        Mask_Adh_Slider.grid(column=0, row=8, sticky='we')
        Mask_Adh_Slider.set(50)

        ## Social distancing slider
        Soc_Dist = IntVar()
        SD_label = ttk.Label(mainframe)
        SD_label.grid(column=0, row=9, sticky='we')

        def update_lbl_SD(Soc_Dist):
            SD_label['text'] = "Social distancing adherence: " + Soc_Dist + "%"
        Soc_Dist_Slider = ttk.Scale(mainframe, orient='horizontal', length=200, from_=0.0, to=100.0, variable=Soc_Dist,command=update_lbl_SD)
        Soc_Dist_Slider.grid(column=0, row=10, sticky='we')
        Soc_Dist_Slider.set(50)

        ## Office plan listbox
        Office_Plans = ["Floor 1", "Floor 2", "Floor 3", "Floor 4"]
        office_plans_var = StringVar(value=Office_Plans)
        Office_Plans_Listbox = Listbox(mainframe, listvariable=office_plans_var, height=4)
        Office_Plans_Listbox.grid(column=0, row=11, sticky='we')

        ##scalling to add space arround widdgets
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

root = Tk()
GUI(root)
root.mainloop()