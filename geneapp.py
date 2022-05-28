import tkinter as tk
from tkinter import Toplevel, ttk, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import datetime as dt


# Global Variables
root = tk.Tk() # Create Root Window
subwindow = None # Sub window
livingMales = []
deadMales = []
livingFemales = []
deadFemales = []
T = nx.DiGraph() #δημιουργία κενού δικτύου
buffer = "ID,Name,Birth,Death,Sex,Father,Mother,Description\n"


def on_save():
    """ Γράφει τα δεδομένα του buffer σε ένα υπάρχων ή νέο αρχείο που θα καθορίσει ο χρήστης. """
    # Update Status Text
    update_status("Αποθήκευση...")
    # Grab Path and Filename to save
    save_dir = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("GeneApp CSV File", "*.csv"), ("All files", "*")))
    # Try to see if save directory is valid to save
    try:
        with open(save_dir, "w", encoding="utf-8") as f:
            f.write(buffer)
        update_status("Αποθηκεύτηκε!")
    except:
        update_status("Αποθήκευση απέτυχε!")


def on_load():
    """ Φορτώνει ένα αρχείο, ελέγχει τη δομή του, και τελικά προσθέτει το περιεχόμενό του στον buffer. """
    # Update Status Text
    update_status("Φόρτωση από...")
    # Get path of file to Load in a temporary variable
    load_path = filedialog.askopenfilename(filetypes = (("GeneApp CSV", "*.csv"), ("All files", "*")))
    # Check if temporary path is okay and load it or not
    if load_path != "":
        update_status("Αρχείο φορτώθηκε! Έλεγχος δομής του αρχείου...")
        # Open the file for check
        with open(load_path, encoding="utf-8") as f:
            # Pre-check if header is compatible with our data structure
            try:
                hd = f.readlines()[0].replace("\n","").split(",")
                template = ["ID","Name","Birth","Death","Sex","Father","Mother","Description"]
                # Data structure seems OK
                if hd == template:
                    root.after(1200, update_status, "Η δομή φαίνεται σωστή. Ο Buffer φορτώθηκε!")
                else:
                    root.after(1200, update_status, "Η δομή του αρχείου είναι μη εγκύρη!")
                    return
            except:
                root.after(1200, update_status, "Το αρχείο είναι μη αναγνώσιμο ή κατεστραμμένο!")
                return
        # If we made it this far, file is probably OK
        global buffer
        # Clear the buffer (preventing duplicate records)
        buffer = ""
        # Write contents to buffer
        with open(load_path, encoding="utf-8") as f:
            for line in f.readlines():
                buffer += line
    else:
        update_status("Η φόρτωση απέτυχε...")


def create_interface():
    ''' Δημιουργεί το βασικό GUI της εφαρμογής. '''
    # Set Root's Window Properties
    root.title("GeneApp - Εφαρμογή Γενεαλογικού Δέντρου")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    # Create App Frame
    app = tk.Frame(root)
    # Heading
    intro = ttk.Label(app,
        text="GeneApp - Εφαρμογή Γενεαλογικού Δέντρου",
        font=("Arial 16"), foreground="#151515",
    )
    # Status Bar
    global status_var
    status_var = tk.StringVar()
    status = ttk.Label(root,
        textvariable=status_var,
        foreground="#151515", background="#ddd", padding=5
    )
    # Insert Person
    insert_btn = ttk.Button(app, text="Εισαγωγή", command=on_insert)
    insert_lbl = ttk.Label(app,
        text="Εισάγετε νέο άτομο στο Γενεαλογικό Δέντρο ή επεξεργαστείτε ένα υπάρχων.",
        font=("Arial 12"), foreground="#151515", background="#ddd"
    )
    # Delete Person
    delete_btn = ttk.Button(app, text="Διαγραφή", command=on_delete)
    delete_lbl = ttk.Label(app,
        text="Αφαιρέστε ένα άτομο από το Γενεαλογικό Δέντρο.",
        font=("Arial 12"), background="#ddd", foreground="#151515"
    )
    # View Graph Tree
    view_btn = ttk.Button(app, text="Προβολή Δέντρου", command=on_view)
    view_lbl = ttk.Label(app,
        text="Προβολή ενός γράφου του Γενεαλογικού Δέντρου.",
        font=("Arial 12"), background="#ddd", foreground="#151515"
    )
    # Save Button
    save_btn = ttk.Button(app, text="Αποθήκευση...", command=on_save)
    # Load Button
    load_btn = ttk.Button(app, text="Άνοιγμα από...", command=on_load)
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


def on_insert():
    ''' Συνάρτηση που τρέχει όταν πατηθεί το κουμπί "Προσθήκη". '''
    global subwindow
    # Do not allow multiple sub windows to be opened
    if subwindow == None or not tk.Toplevel.winfo_exists(subwindow):
        # Create subwindow and define its properties
        subwindow = tk.Toplevel(root)
        subwindow.title("GeneApp - Genealogy Tree Application")
        subwindow.columnconfigure(0, weight=1)
        subwindow.rowconfigure(0, weight=1)
        # Create a frame wrapper inside subwindow
        wrapper = ttk.Frame(subwindow)
        ## Create the form
        # ID
        ttk.Label(wrapper, text="ID", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.E)
        id = tk.IntVar(value=get_ID(buffer))
        ttk.Entry(wrapper, textvariable=id).grid(row=0, column=4, columnspan=6, padx=8, pady=4)
        # Name
        ttk.Label(wrapper, text="Ονοματεπώνυμο", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=1, column=0, columnspan=4, sticky=tk.W + tk.E)
        name = tk.StringVar()
        ttk.Entry(wrapper, textvariable=name).grid(row=1, column=4, columnspan=6, padx=8, pady=4)
        # Birth Date
        ttk.Label(wrapper, text="Ημερομηνία Γέννησης", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=2, column=0, columnspan=4, sticky=tk.W + tk.E)
        birth = tk.StringVar()
        ttk.Entry(wrapper, textvariable=birth).grid(row=2, column=4, columnspan=6, padx=8, pady=4)
        # Death Date
        ttk.Label(wrapper, text="Ημερομηνία Θανάτου", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=3, column=0, columnspan=4, sticky=tk.W + tk.E)
        death = tk.StringVar()
        ttk.Entry(wrapper, textvariable=death).grid(row=3, column=4, columnspan=6, padx=8, pady=4)
        # Sex
        ttk.Label(wrapper, text="Φύλο", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=4, column=0, columnspan=4, sticky=tk.W + tk.E)
        sex_box = tk.Frame(wrapper)
        sex = tk.IntVar(value=0)
        male = ttk.Radiobutton(sex_box, text="Male", variable=sex, value=1).grid(row=0, column=0)
        female = ttk.Radiobutton(sex_box, text="Female", variable=sex, value=2).grid(row=0, column=1)
        sex_box.grid(row=4, column=4, columnspan=6, padx=8, pady=4)
        # Father ID
        ttk.Label(wrapper, text="ID Πατέρα", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=5, column=0, columnspan=4, sticky=tk.W + tk.E)
        f_ID = tk.StringVar()
        ttk.Entry(wrapper, textvariable=f_ID).grid(row=5, column=4, columnspan=6, padx=8, pady=4)
        # Mother ID
        ttk.Label(wrapper, text="ID Μητέρας", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=6, column=0, columnspan=4, sticky=tk.W + tk.E)
        m_ID = tk.StringVar()
        ttk.Entry(wrapper, textvariable=m_ID).grid(row=6, column=4, columnspan=6, padx=8, pady=4)
        # Description
        ttk.Label(wrapper, text="Περιγραφή", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=7, column=0, columnspan=5, sticky=tk.W + tk.E)
        desc = tk.Text(wrapper, spacing1=2, spacing2=3, undo=True, maxundo=10, wrap='char', height=2, width=35)
        desc.grid(row=8, column=0, columnspan=5, sticky=tk.W + tk.E, pady=4)
        # Submit Button
        ttk.Button(wrapper, text="Προσθήκη", command=lambda: on_submit(str(id.get()), str(name.get()), str(birth.get()), str(death.get()), str(sex.get()), str(f_ID.get()), str(m_ID.get()), desc.get('1.0','end-1c'))).grid(row=9)
        # Place wrapper (frame) in the root window
        wrapper.grid(padx=14, pady=14)


def on_print():
    ''' Εκτυπώνει κάποιες πληροφορίες για debugging λόγους. '''
    print("--- --- --- ---")
    print("Buffer: \n" + buffer)
    print("--- --- --- ---\n")
    print("LivingMales: \n")
    for lMale in livingMales:
        print(lMale)
    print("--- --- --- ---\n")
    print("DeadMales: \n")
    for dMale in deadMales:
        print(dMale)
    print("--- --- --- ---\n")
    print("LivingFemales: \n")
    for lFemale in livingFemales:
        print(lFemale)
    print("--- --- --- ---\n")
    print("DeadFemales: \n")
    for dFemale in deadFemales:
        print(dFemale)


def on_submit(id, name, birth, death, sex, f_ID, m_ID, desc):
    ''' Συνάρτηση που τρέχει όταν πατήσει ο χρήστης το κουμπί submit στην προσθήκη νέου ατόμου. '''
    global buffer

    # Έλεγχος 1: ID να είναι int και unique (το ID=0 αντιστοιχεί στον άγνωστο γονέα)
    try:
        if int(id) in get_IDs(buffer):
            update_status("Υπάρχει ήδη άτομο με αυτό το ID!")
            return
    except:
        pass

    # Έλεγχος 2: Αν δώθηκε ονομασία και είναι με λατινικούς χαρακτήρες
    if name == "" or name.isascii() == False:
        update_status("Εισάγετε ονομασία του ατόμου με λατινικούς χαρακτήρες.")
        return

    # Έλεγχος 3: Μετατροπή και έλεγχος birth και death σε date_format και σύγκριση αν death > birth
    if death: # Αν υπάρχει ημερομηνία Θανάτου
        try:
            if dt.date(int(death.split("/")[2]),int(death.split("/")[1]),int(death.split("/")[0])) <= dt.date(int(birth.split("/")[2]),int(birth.split("/")[1]),int(birth.split("/")[0])):
                update_status("Η ημερομηνία γέννησης πρέπει να είναι μικρότερη της ημερομηνίας θανάτου.")
                return
        except:
            update_status('Οι ημερομηνίες πρέπει να είναι της μορφης "d/m/y"!')
            return
    else:
        try:
            dt.date(int(birth.split("/")[2]),int(birth.split("/")[1]),int(birth.split("/")[0]))
        except:
            update_status('Η ημερομηνία γέννησης πρέπει να είναι της μορφής "d/m/y"!')
            return

    # Έλεγχος 4: Αν δώθηκε φύλο
    if int(sex) == 0:
        update_status("Επιλέξτε το φύλο του ατόμου.")
        return

    # Έλεγχος 5: f_ID και m_ID να είναι int και να υπάρχουν (αν δώθηκαν) αλλιώς τα θέτουμε 0
    if f_ID:
        try:
            if int(f_ID) not in get_IDs(buffer):
                update_status("Δεν υπάρχει το ID του πατέρα!")
                return
        except:
            update_status("Δεν δώθηκε αριθμός για ID πατέρα!")
            return
    else:
        f_ID = "0" # Άγνωστος Πατέρας
    if m_ID:
        try:
            if int(m_ID) not in get_IDs(buffer):
                update_status("Δεν υπάρχει το ID της μητέρας!")
                return
        except:
            update_status("Δεν δώθηκε αριθμός για ID μητέρας!")
            return
    else:
        m_ID = "0" # Άγνωστη Μητέρα
    
    # Έλεγχος 6: Διάφορες συγγενικές σχέσεις
    if not valid(int(f_ID), int(m_ID)): return

    # Τα δεδομένα μας είναι ΟΚ, εισάγουμε τον χρήστη
    buffer += id+","+name+","+birth+","+death+","+sex+","+f_ID+","+m_ID+","+desc+"\n"
    # Destroy Subwindow and allow to be recreated
    subwindow.destroy()
    # Update Status Message
    update_status("Προστέθηκε ένα άτομο!")


def valid(id_1, id_2):
    ''' Συνάρτηση που δέχεται 2 ID (πατέρα, μητέρα) και ελέγχει αν είναι ΟΚ η γέννηση παιδιού. '''
    data = pd.read_csv(StringIO(buffer), index_col=0)
    data["Death"]=data["Death"].astype(str)

    # Έλεγχος αν τα IDs είναι διαφορετικού φύλου
    if id_1 != 0 and id_2 != 0: # Εφόσον υπάρχουν και πατέρας και μητέρα
        if buffer.split("\n")[id_1].split(",")[4] == buffer.split("\n")[id_2].split(",")[4]:
            update_status("Οι γονείς πρέπει να είναι διαφορετικού φύλου!")
            return False

    # Έλεγχος αν τα IDs έχουν σχέση παιδιού-γονέα

    # Έλεγχος αν τα IDs είναι αδέρφια

    # Έλεγχος αν τα IDs είναι ξαδέρφια

    # Έλεγχος αν τα IDs είναι δεύτερα ξαδέρφια

    # Όλες οι σχέσεις ΟΚ
    return True


def update_status(txt):
    ''' Ανανεώνει το μήνυμα κατάστασης στην κάτω μπάρα της εφαρμογής. '''
    status_var.set(txt)


def on_delete():
    ''' Συνάρτηση που τρέχει όταν πατηθεί το κουμπί delete. '''
    global subwindow
    # Do not allow multiple sub windows to be opened
    if subwindow == None or not tk.Toplevel.winfo_exists(subwindow):
        # Create subwindow and define its properties
        subwindow = tk.Toplevel(root)
        subwindow.title("GeneApp - Genealogy Tree Application")
        subwindow.columnconfigure(0, weight=1)
        subwindow.rowconfigure(0, weight=1)
        # Create a frame wrapper inside subwindow
        wrapper = ttk.Frame(subwindow)
        ttk.Label(wrapper, text="Όνομα", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=0,column=0, columnspan=4, sticky=tk.W + tk.E)
        ID = tk.IntVar()
        ttk.Entry(wrapper, textvariable=ID).grid(row=0, column=4, columnspan=6, padx=8, pady=4)
        ttk.Button(wrapper, text="Εντάξει", command="").grid(row=9)
        ttk.Button(wrapper, text="Έξοδος", command="").grid(row=9, column=4)
        wrapper.grid(padx=14, pady=14)


def get_ID(buffer):
    ''' Συνάρτηση που δέχεται το String του Buffer και βρίσκει το αμέσως επόμενο διαθέσιμο ID. '''
    try:
        return int(buffer.split("\n")[-2].split(",")[0])+1 #[-2] γιατί το τελευταίο στοιχείο της λίστας είναι το κενό (\n)
    except:
        return 1 # Άδειο Buffer, λογικά περιέχει μόνο τα headers, άρα επιστρέφουμε για ID το 1 (το 0 είναι κρατημένο ως "κανένας γονέας").


def get_IDs(buffer):
    ''' Συνάρτηση που δέχεται το String του Buffer και γυρνάει όλα τα IDs σε μια λίστα (+ το 0 το οποίο αντιστοιχεί στον άγνωστο γονέα). '''
    IDs = []
    IDs.append(0)
    try:
        [IDs.append(int(record.split(",")[0])) for record in buffer.split("\n")[1:-1]] #[1:-1] γιατί το πρώτο στοιχείο είναι το "ID" και το τελευταίο το κενό (\n)
        return IDs
    except:
        print("Δεν μπόρεσε να δημιουργηθεί λίστα με όλα τα IDs.")


def on_view():
    ''' Συνάρτηση που τρέχει όταν ο χρήστης πατήσει το κουμπί της προβολής δέντρου. '''
    data = pd.read_csv(StringIO(buffer), index_col=0)
    data["Death"]=data["Death"].astype(str)

    # Καθάρισμα όλων των λιστών
    livingMales.clear()
    deadMales.clear()
    livingFemales.clear()
    deadFemales.clear()

    # Προσθήκη Κορυφών και δημιουργία λιστών
    for person in data.index:
        newNode = data.loc[person, "Name"]
        if data.loc[person, "Sex"] == 1:
            if data.loc[person, "Death"]=="nan":
                livingMales.append(newNode)
            else:
                deadMales.append(newNode)
        else:
            if data.loc[person, "Death"]=="nan":
                livingFemales.append(newNode)
            else:
                deadFemales.append(newNode)
        T.add_node(newNode)

    # Προσθήκη Ακμών
    for person in data.index:
        if data.loc[person, "Father"] != 0:
            personsFatherNumber = data.loc[person, "Father"]
            personsFather = data.loc[personsFatherNumber, 'Name']
            v = personsFather
            u = data.loc[person, "Name"]
            T.add_edge(v, u)
        if data.loc[person, "Mother"] != 0:
            personsMotherNumber = data.loc[person, "Mother"]
            personsMother = data.loc[personsMotherNumber, "Name"]
            v = personsMother
            u = data.loc[person, "Name"]
            T.add_edge(v, u)
    
    # Σχεδίαση Γράφου
    pos = graphviz_layout(T, prog="dot")

    nx.draw_networkx_nodes(T, pos, nodelist=livingMales, node_color="tab:blue", alpha = 1.0)
    nx.draw_networkx_nodes(T, pos, nodelist=deadMales, node_color="tab:blue", alpha = 0.2)
    nx.draw_networkx_nodes(T, pos, nodelist=livingFemales, node_color="tab:red", alpha = 1.0)
    nx.draw_networkx_nodes(T, pos, nodelist=deadFemales, node_color="tab:red", alpha = 0.2)

    nx.draw_networkx_labels(T, pos, labels = {n: n for n in livingMales}, alpha = 1.0)
    nx.draw_networkx_labels(T, pos, labels = {n: n for n in deadMales}, alpha = 0.2)
    nx.draw_networkx_labels(T, pos, labels = {n: n for n in livingFemales}, alpha = 1.0)
    nx.draw_networkx_labels(T, pos, labels = {n: n for n in deadFemales}, alpha = 0.2)

    nx.draw_networkx_edges(T, pos)
    plt.show()


create_interface()
