# main.py
""" Main GUI Application for Tkinter """
from socket import timeout
import tkinter as tk
from tkinter import ttk
from datetime import datetime as dt
from pathlib import Path
import csv


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
insert_btn = ttk.Button(app, text="Insert")
insert_lbl = ttk.Label(
    app,
    text="Insert a new person in the Genealogy Tree or edit an existing one.",
    font=("Arial 12"),
    foreground="#151515",
    background="#ddd"
)


# Delete Person
delete_btn = ttk.Button(app, text="Delete")
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


# Save
def on_save():
    """To be run when the user tries to save progress"""
    # Get Date Formatted String
    datestring = dt.today().strftime("%Y-%m-%d")
    # Generate Filename
    filename = f"geneapp_{datestring}.csv"
    # Check if filename exists in executable's path
    newfile = not Path(filename).exists()
    # Update Status Text
    status_var.set("Saving...")
    with open(filename, 'a', newline='') as fh:
        csvwriter = csv.DictWriter(fh, fieldnames=["ID","First","Last","Birth","Description","Connections"])
        if newfile:
            csvwriter.writeheader()
        csvwriter.writerow({"ID":1,"First":"Takis","Last":"Takitzis","Birth":"2/2/1990","Description":"Takis is a cool guy!","Connections":"1/3/5"})
        done = True
    if done:
        status_var.set("Saved!")

save_btn = ttk.Button(app, text="Save", command=on_save)


# Load
load_btn = ttk.Button(app, text="Load")


# Place Widgets in App Frame
intro.grid(row=0, columnspan=10, sticky=tk.W + tk.E, pady=10)
insert_btn.grid(row=1, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
insert_lbl.grid(row=1, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
delete_btn.grid(row=2, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
delete_lbl.grid(row=2, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
view_btn.grid(row=3, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
view_lbl.grid(row=3, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
save_btn.grid(row=4, column=8, sticky=tk.W + tk.E, pady=4, padx=4)
load_btn.grid(row=4, column=9, sticky=tk.W + tk.E, pady=4, padx=4)


# Place Frame in Root Window
app.grid(padx=14, pady=14)
status.grid(sticky=tk.W + tk.E)


# Start event loop
root.mainloop()