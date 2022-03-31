# buttons.py
""" File that includes the InsertPerson class which creates the button "Insert" and all its functions. """
import tkinter as tk
from tkinter import Toplevel, ttk, filedialog


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
        self.alive = False


    def open(self):
        """ Opens the insert person window and display the form. """

        # Do not allow multiple sub windows to be opened
        if self.subwindow == None or not tk.Toplevel.winfo_exists(self.subwindow) and self.alive == False:

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
                # Firstname
                ttk.Label(wrapper, text="First", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=1, column=0, columnspan=4, sticky=tk.W + tk.E)
                self.first = tk.StringVar()
                ttk.Entry(wrapper, textvariable=self.first).grid(row=1, column=4, columnspan=6, padx=8, pady=4)
                # Submit Button
                ttk.Button(wrapper, text="Submit", command=self.on_submit).grid(row=6)
            
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

        if tk.Toplevel.winfo_exists(self.subwindow):
            self.alive = True
            self.statusbar.set("Inserting new person...")

        else:
            self.alive = False
            self.statusbar.set("New person inserted!")

        self.master.after(1000, self.update_status)


    def on_submit(self):
        """ Triggers when user hits the submit button """

        print( str(self.ID.get()) +"\n"+ str(self.first.get()) )
        