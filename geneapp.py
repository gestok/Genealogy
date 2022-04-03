#geneapp.py
"""Main Application File"""
import tkinter as tk
from tkinter import Toplevel, ttk, filedialog
from datetime import datetime as dt
from pathlib import Path
import pandas
import io
from classes.buttons import GeneButton


# Global Variables
load_path = ""
livingMales = []
deadMales = []
livingFemales = []
deadFemales = []


# Create Root Window
root = tk.Tk()
# Set Root's Window Properties
root.title("GeneApp - Genealogy Tree Application")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# Create App Frame
app = tk.Frame(root)


# Heading
intro = ttk.Label(
    app,
    text="GeneApp - Genealogy Tree Application",
    font=("Arial 16"),
    foreground="#151515",
)


# Status Bar
status_var = tk.StringVar()
status = ttk.Label(
    root,
    textvariable=status_var,
    foreground="#151515",
    background="#ddd",
    padding=5
)


# Insert Person
insert_btn = ttk.Button(app, text="Insert", command=GeneButton(root, status_var, "insert", load_path).open)
insert_lbl = ttk.Label(
    app,
    text="Insert a new person in the Genealogy Tree or edit an existing one.",
    font=("Arial 12"),
    foreground="#151515",
    background="#ddd"
)


# Delete Person
delete_btn = ttk.Button(app, text="Delete", command=GeneButton(root, status_var, "delete", load_path).open)
delete_lbl = ttk.Label(
    app,
    text="Delete an existing person from the Genealogy Tree.",
    font=("Arial 12"),
    background="#ddd",
    foreground="#151515"
)


# View Graph Tree
view_btn = ttk.Button(app, text="View Tree")
view_lbl = ttk.Label(
    app,
    text="View a network graph of the current Genealogy Tree.",
    font=("Arial 12"),
    background="#ddd",
    foreground="#151515"
)


# On Save
def on_save():
    """To be run when the user tries to save progress"""

    # Update Status Text
    status_var.set("Saving...")
    # Grab Path and Filename to save
    save_dir = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("GeneApp CSV File", "*.csv"), ("All files", "*")))

    # Try to see if Path and Filename are set, and if load_path exists
    try:
        if Path(save_dir).exists() or type(save_dir) == str:
            # Save the Data as CSV
            data = pandas.read_csv(filepath_or_buffer=load_path, parse_dates=["Birth","Death"], index_col=["ID"])
            data.to_csv(save_dir)
            # Success
            status_var.set("Saved!")
    except:
        # Failure
        status_var.set("Saving failed!")

# Save Button
save_btn = ttk.Button(app, text="Save...", command=on_save)


# Load Records from given file (should go to the class of "view graph")
# data = pandas.read_csv(load_file, parse_dates=["Birth","Death"])
# data.set_index(['ID'])

# Get the path of the file to load
def on_load():
    """To be run when the user tries to load progress"""

    global load_path

    # Update Status Text
    status_var.set("Loading from...")

    # Get path of file to Load in a temporary variable
    load_path_tmp = filedialog.askopenfilename(filetypes = (("GeneApp CSV", "*.csv"), ("All files", "*")))

    # Check if temporary path is okay and load it or not
    if load_path_tmp != "":
        load_path = load_path_tmp
        status_var.set("Loaded!")

    else:
        status_var.set("Loading failed...")

# Load Button
load_btn = ttk.Button(app, text="Load from...", command=on_load)


# Debugging
def on_print():
    print("Load path: " + str(load_path))


# Place Widgets in App Frame
intro.grid(row=0, columnspan=10, sticky=tk.W + tk.E, pady=10)
insert_btn.grid(row=1, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
insert_lbl.grid(row=1, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
delete_btn.grid(row=2, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
delete_lbl.grid(row=2, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
view_btn.grid(row=3, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
view_lbl.grid(row=3, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
ttk.Button(app, text="Debug", command=on_print).grid(row=4, column=7, sticky=tk.W + tk.E, pady=4, padx=4)
save_btn.grid(row=4, column=8, sticky=tk.W + tk.E, pady=4, padx=4)
load_btn.grid(row=4, column=9, sticky=tk.W + tk.E, pady=4, padx=4)


# Place Frame in Root Window
app.grid(padx=14, pady=14)
status.grid(sticky=tk.W + tk.E)


# Start event loop
root.mainloop()