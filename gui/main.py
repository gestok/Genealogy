# main.py
""" Main GUI Application for Tkinter """
import tkinter as tk

# Create Root Window
root = tk.Tk()

# Set Root's Window Title, Size and Position
root.title("GeneApp - Genealogy Tree Application")
root.geometry("640x480+300+300")
root.resizable(False, False)

# Information
intro = tk.Label(
    root,
    text="GeneApp - Genealogy Tree Application",
    font=("Arial 16"),
    fg="#151515"
)

# Insert Person
insert_btn = tk.Button(root, text="Insert")
insert_lbl = tk.Label(
    root,
    text="Insert a new person in the Genealogy Tree or edit an existing one.",
    font=("Arial 12"),
    bg="#ddd",
    fg="#151515"
)

# Delete Person
delete_btn = tk.Button(root, text="Delete")
delete_lbl = tk.Label(
    root,
    text="Delete an existing person from the Genealogy Tree.",
    font=("Arial 12"),
    bg="#ddd",
    fg="#151515"
)

# View Graph Tree
view_btn = tk.Button(root, text="View Tree")
view_lbl = tk.Label(
    root,
    text="View a network graph of the current Genealogy Tree.",
    font=("Arial 12"),
    bg="#ddd",
    fg="#151515"
)

# Save
save_btn = tk.Button(root, text="Save")
save_output = tk.Label(root, text="")

# Load
load_btn = tk.Button(root, text="Load")

# Place Widgets
intro.grid(row=0, column=0, columnspan=6, sticky="we")
insert_btn.grid(row=1, column=0, columnspan=2, sticky="we")
insert_lbl.grid(row=1, column=2, columnspan=4, sticky="we")
delete_btn.grid(row=2, column=0, columnspan=2, sticky="we")
delete_lbl.grid(row=2, column=2, columnspan=4, sticky="we")
view_btn.grid(row=3, column=0, columnspan=2, sticky="we")
view_lbl.grid(row=3, column=2, columnspan=4, sticky="we")
# save_btn.grid(row=4 )

# Start event loop
root.mainloop()