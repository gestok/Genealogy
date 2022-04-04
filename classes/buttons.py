# buttons.py
""" File that includes the InsertPerson class which creates the button "Insert" and all its functions. """
import tkinter as tk
from tkinter import Toplevel, ttk, filedialog
from numpy import spacing


class GeneButton(ttk.Frame):
    """ Button Class. """

    def __init__(self, master, statusbar, functionality, path_to_csv):
        """ Master is defined as the root element, statusbar is the main application's status bar. """

        ttk.Frame.__init__(self, master)
        self.master = master
        self.statusbar = statusbar
        self.functionality = str(functionality).lower()
        self.path = path_to_csv
        self.subwindow = None


    def open(self):
        """ Opens the insert person window and display the form. """

        # Do not allow multiple sub windows to be opened
        if self.subwindow == None or not tk.Toplevel.winfo_exists(self.subwindow):

            # Create subwindow and define its properties
            self.subwindow = tk.Toplevel(self.master)
            self.subwindow.title("GeneApp - Genealogy Tree Application")
            self.subwindow.columnconfigure(0, weight=1)
            self.subwindow.rowconfigure(0, weight=1)

            # Create a frame wrapper inside subwindow
            wrapper = ttk.Frame(self.subwindow)

            # Create the appropriate form
            if self.functionality == "insert":
                # ID
                ttk.Label(wrapper, text="ID", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.E)
                self.ID = tk.IntVar()
                ttk.Entry(wrapper, textvariable=self.ID).grid(row=0, column=4, columnspan=6, padx=8, pady=4)
                # Name
                ttk.Label(wrapper, text="Name", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=1, column=0, columnspan=4, sticky=tk.W + tk.E)
                self.name = tk.StringVar()
                ttk.Entry(wrapper, textvariable=self.name).grid(row=1, column=4, columnspan=6, padx=8, pady=4)
                # Birth Date
                ttk.Label(wrapper, text="Birth Date", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=2, column=0, columnspan=4, sticky=tk.W + tk.E)
                self.birth = tk.StringVar()
                ttk.Entry(wrapper, textvariable=self.birth).grid(row=2, column=4, columnspan=6, padx=8, pady=4)
                # Death Date
                ttk.Label(wrapper, text="Death Date", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=3, column=0, columnspan=4, sticky=tk.W + tk.E)
                self.death = tk.StringVar()
                ttk.Entry(wrapper, textvariable=self.death).grid(row=3, column=4, columnspan=6, padx=8, pady=4)
                # Sex
                ttk.Label(wrapper, text="Sex", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=4, column=0, columnspan=4, sticky=tk.W + tk.E)
                sex_box = tk.Frame(wrapper)
                self.sex = tk.IntVar()
                male = ttk.Radiobutton(sex_box, text="Male", variable=self.sex, value=1).grid(row=0, column=0)
                female = ttk.Radiobutton(sex_box, text="Female", variable=self.sex, value=2).grid(row=0, column=1)
                sex_box.grid(row=4, column=4, columnspan=6, padx=8, pady=4)
                # Father ID
                ttk.Label(wrapper, text="Father ID", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=5, column=0, columnspan=4, sticky=tk.W + tk.E)
                self.f_ID = tk.IntVar()
                ttk.Entry(wrapper, textvariable=self.f_ID).grid(row=5, column=4, columnspan=6, padx=8, pady=4)
                # Mother ID
                ttk.Label(wrapper, text="Mother ID", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=6, column=0, columnspan=4, sticky=tk.W + tk.E)
                self.m_ID = tk.IntVar()
                ttk.Entry(wrapper, textvariable=self.m_ID).grid(row=6, column=4, columnspan=6, padx=8, pady=4)
                # Description
                ttk.Label(wrapper, text="Description", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=7, column=0, columnspan=5, sticky=tk.W + tk.E)
                self.desc = tk.Text(wrapper, spacing1=2, spacing2=3, undo=True, maxundo=10, wrap='char', height=2, width=27)
                self.desc.grid(row=8, column=0, columnspan=5, sticky=tk.W + tk.E, pady=4)
                # Submit Button
                ttk.Button(wrapper, text="Submit", command=self.on_submit).grid(row=9)
            
            elif self.functionality == "delete":
                pass

            elif self.functionality == "view":
                pass

            else:
                print("Uknown Functionality defined!")

            # Place wrapper (frame) in the root window
            wrapper.grid(padx=14, pady=14)

            # Update Status Message
            self.update_status()


    def update_status(self):
        """ Updates status messages on main application. """
        if self.subwindow == None:
            return

        if tk.Toplevel.winfo_exists(self.subwindow):
            self.statusbar.set("Inserting new person...")
        else:
            self.statusbar.set("New person inserted!")

        self.master.after(1000, self.update_status)


    def on_submit(self):
        """ Triggers when user hits the submit button. """

        print( str(self.ID.get()) +"\n"+ str(self.name.get()) +"\n"+ str(self.birth.get()) +"\n"+ str(self.death.get()) +"\n"+ str(self.sex.get()) +"\n"+ str(self.f_ID.get()) +"\n"+ str(self.m_ID.get()) +"\n"+ str(self.desc.get("1.0","end-1c")) )
        