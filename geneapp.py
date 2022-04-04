#geneapp.py
"""Main Application File"""
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from classes.buttons import GeneButton


# Global Variables
livingMales = []
deadMales = []
livingFemales = []
deadFemales = []
buffer = ""

# Create Root Window
root = tk.Tk()
# Set Root's Window Properties
root.title("GeneApp - Genealogy Tree Application")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# Create App Frame
app = tk.Frame(root)


# Heading
intro = ttk.Label(app,
    text="GeneApp - Genealogy Tree Application",
    font=("Arial 16"), foreground="#151515",
)


# Status Bar
status_var = tk.StringVar()
status = ttk.Label(root,
    textvariable=status_var,
    foreground="#151515", background="#ddd", padding=5
)


# Insert Person
insert_btn = ttk.Button(app, text="Insert", command=GeneButton(root, status_var, "insert", buffer).open)
insert_lbl = ttk.Label(app,
    text="Insert a new person in the Genealogy Tree or edit an existing one.",
    font=("Arial 12"), foreground="#151515", background="#ddd"
)


# Delete Person
delete_btn = ttk.Button(app, text="Delete", command=GeneButton(root, status_var, "delete", buffer).open)
delete_lbl = ttk.Label(app,
    text="Delete an existing person from the Genealogy Tree.",
    font=("Arial 12"), background="#ddd", foreground="#151515"
)


# View Graph Tree
view_btn = ttk.Button(app, text="View Tree", command=GeneButton(root, status_var, "view", buffer).open)
view_lbl = ttk.Label(app,
    text="View a network graph of the current Genealogy Tree.",
    font=("Arial 12"), background="#ddd", foreground="#151515"
)


def on_save():
    """ Writes the contents of buffer to an existing or new file specified by the user. """

    # Update Status Text
    update_status("Saving...")

    # Grab Path and Filename to save
    save_dir = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("GeneApp CSV File", "*.csv"), ("All files", "*")))

    # Try to see if save directory is valid to save
    try:
        with open(save_dir, "w", encoding="utf-8") as f:
            f.write(buffer)
        update_status("Saved!")
    except:
        update_status("Saving failed!")

# Save Button
save_btn = ttk.Button(app, text="Save...", command=on_save)


def on_load():
    """ Loads a file, checks it's data structure, and finally loads it to the buffer. """

    # Update Status Text
    update_status("Loading from...")

    # Get path of file to Load in a temporary variable
    load_path = filedialog.askopenfilename(filetypes = (("GeneApp CSV", "*.csv"), ("All files", "*")))

    # Check if temporary path is okay and load it or not
    if load_path != "":
        update_status("File loaded! Checking data structure from file...")
        # Open the file for check
        with open(load_path, encoding="utf-8") as f:
            # Pre-check if header is compatible with our data structure
            try:
                hd = f.readlines()[0].replace("\n","").split(",")
                template = ["ID","Name","Birth","Death","Sex","Father","Mother","Description"]
                # Data structure seems OK
                if hd == template:
                    root.after(1200, update_status, "Data structure seems correct. Buffer is loaded!")
                else:
                    root.after(1200, update_status, "Incorrect data structure!")
                    return
            except:
                root.after(1200, update_status, "File unreadable or corrupted!")
                return
        
        # If we made it this far, file is probably OK
        # Clear the buffer (preventing duplicate records)
        buffer = ""
        # Write contents to buffer
        with open(load_path, encoding="utf-8") as f:
            for line in f.readlines():
                buffer += line

    else:
        update_status("Loading failed...")
    
    return buffer

# Load Button
load_btn = ttk.Button(app, text="Load from...", command=on_load)


def on_print():
    """ Prints some info for debugging purposes. """
    print("--- --- --- ---")
    print("Load path: " + str(load_path))
    print("--- --- --- ---")
    print("Buffer: \n" + buffer)
    # print(pd.read_csv(load_path))


def update_status(txt):
    """ Updates the status bar message of main application. """
    status_var.set(txt)


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