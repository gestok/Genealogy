import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import datetime as dt
import re
from PIL import ImageTk, Image


# Global Variables
root = tk.Tk() # Create Root Window
subwindow = None # Sub window
livingMales = {}
deadMales = {}
livingFemales = {}
deadFemales = {}
T = nx.DiGraph() #δημιουργία κενού δικτύου
buffer = "ID,Name,Birth,Death,Sex,Father,Mother,Description\n"


def center_window():
    """ Συνάρτηση που κεντράρει το παράθυρο της εφαρμογής. """
    window_height = 729
    window_width = 720
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2)-(window_height/2))
    root.geometry("{}x{}+{}+{}".format(window_width,window_height,x_cordinate,y_cordinate))


def on_save():
    """ Γράφει τα δεδομένα του buffer σε ένα υπάρχων ή νέο αρχείο που θα καθορίσει ο χρήστης. """
    update_status("Αποθήκευση...")
    # Δημιουργία διαδρομής και ονομασίας για αποθήκευση
    save_dir = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("GeneApp CSV File", "*.csv"), ("All files", "*")))
    # Έλεγχος αν η διαδρομή είναι εντάξει για αποθήκευση
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
    load_path = tk.filedialog.askopenfilename(filetypes = (("GeneApp CSV", "*.csv"), ("All files", "*")))
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

    image1 = Image.open("familytree.png")
    test = ImageTk.PhotoImage(image1)
    label1 = tk.Label(image=test)
    label1.image = test
    label1.place(x=0, y=0, relwidth=1, relheight=1)
    def on_resize(event):
        # resize the background image to the size of label
        image = image1.resize((event.width, event.height), Image.ANTIALIAS)
        # update the image of the label
        label1.image = ImageTk.PhotoImage(image)
        label1.config(image=label1.image)
    label1.bind('<Configure>', on_resize)

    # Ιδιότητες Παραθύρου Root
    root.title("GeneApp - Εφαρμογή Γενεαλογικού Δέντρου")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    center_window()

    # Δημιουργία ενός wrapper frame για το Application
    app = tk.Frame(root)
    # Τίτλος
    intro = ttk.Label(app,
        text="GeneApp - Εφαρμογή Γενεαλογικού Δέντρου",
        font=("Arial 16"), foreground="#151515",
    )
    # Μπάρα Κατάστασης
    global status_var
    status_var = tk.StringVar()
    status = ttk.Label(root,
        textvariable=status_var,
        foreground="#151515", background="#ddd", padding=5
    )
    # Εισαγωγή Ατόμου
    insert_btn = ttk.Button(app, text="Εισαγωγή", command=on_insert)
    insert_lbl = ttk.Label(app,
        text="Εισάγετε νέο άτομο στο Γενεαλογικό Δέντρο ή επεξεργαστείτε ένα υπάρχων.",
        font=("Arial 12"), foreground="#151515", background="#ddd"
    )
    # Διαγραφή Ατόμου
    delete_btn = ttk.Button(app, text="Διαγραφή", command=on_delete)
    delete_lbl = ttk.Label(app,
        text="Αφαιρέστε ένα άτομο από το Γενεαλογικό Δέντρο.",
        font=("Arial 12"), background="#ddd", foreground="#151515"
    )
    # Προβολή Γράφου
    view_btn = ttk.Button(app, text="Προβολή Δέντρου", command=on_view)
    view_lbl = ttk.Label(app,
        text="Προβολή ενός γράφου του Γενεαλογικού Δέντρου.",
        font=("Arial 12"), background="#ddd", foreground="#151515"
    )
    # Κουμπί Εκκαθάρισης
    unload_btn = ttk.Button(app, text="Διαγραφή Δέντρου", command=on_unload)
    unload_lbl=ttk.Label(app,
        text="Διαγραφή του Γενεαλογικού Δέντρου. ",
        font=("Arial 12"), background="#ddd", foreground="#151515"
    )
    # Κουμπί Αποθήκευσης
    save_btn = ttk.Button(app, text="Αποθήκευση...", command=on_save)
    # Κουμπί Φόρτωσης
    load_btn = ttk.Button(app, text="Άνοιγμα από...", command=on_load)
    # Τοποθέτηση των Widget στο Application Frame
    intro.grid(row=0, columnspan=10, sticky=tk.W + tk.E, pady=10)
    insert_btn.grid(row=1, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
    insert_lbl.grid(row=1, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
    delete_btn.grid(row=2, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
    delete_lbl.grid(row=2, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
    view_btn.grid(row=3, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
    view_lbl.grid(row=3, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
    unload_btn.grid(row=4, columnspan=4, sticky=tk.W + tk.E, pady=4, padx=4)
    unload_lbl.grid(row=4, column=4, columnspan=6, sticky=tk.W + tk.E, pady=4, padx=4)
    save_btn.grid(row=5, column=8, sticky=tk.W + tk.E, pady=4, padx=4)
    load_btn.grid(row=5, column=9, sticky=tk.W + tk.E, pady=4, padx=4)
    # Τοποθέτηση του Application Frame στο Root παράθυρο
    app.grid(padx=14, pady=14)
    status.grid(sticky=tk.W + tk.E)
    # Εισαγωγή window icon για την εφαρμογή.
    root.iconbitmap('favicon.ico')
    # Εκκίνηση του interface
    root.mainloop()


def on_insert():
    ''' Συνάρτηση που τρέχει όταν πατηθεί το κουμπί "Προσθήκη". '''
    global subwindow

    # Δεν επιτρέπουμε την πολλαπλή δημιουργία υποπαραθύρων
    if subwindow == None or not tk.Toplevel.winfo_exists(subwindow):
        # Δημιουργία υποπαραθύρου και ορισμός των μεταβλητών του
        subwindow = tk.Toplevel(root)
        subwindow.title("GeneApp - Genealogy Tree Application")
        subwindow.columnconfigure(0, weight=1)
        subwindow.rowconfigure(0, weight=1)
        subwindow.geometry('330x330+750+300')
        subwindow.iconbitmap('favicon.ico')

        # Δημιουργία frame wrapper εντός του υποπαραθύρου
        wrapper = ttk.Frame(subwindow)
        ## Δημιουργία της φόρμας
        # ID
        ttk.Label(wrapper, text="ID", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=0, column=0, columnspan=4, sticky=tk.W + tk.E)
        id = tk.StringVar(value=get_ID())
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
        ttk.Button(wrapper, text="Προσθήκη", command=lambda: on_submit(wrapper, T, str(id.get()), str(name.get()), str(birth.get()), str(death.get()), str(sex.get()), str(f_ID.get()), str(m_ID.get()), desc.get('1.0','end-1c'))).grid(row=9)
        # Τοποθέτηση του frame wrapper στο root παράθυρο
        wrapper.grid(padx=14, pady=14)

        update_status("Εισαγωγή ατόμου...")


def on_submit(wrapper, network, id, name, birth, death, sex, f_ID, m_ID, desc):
    ''' Συνάρτηση που τρέχει όταν πατήσει ο χρήστης το κουμπί submit στην προσθήκη νέου ατόμου. '''
    global buffer
    replacing = False

    # Έλεγχος 1: ID να είναι int και unique (το ID=0 αντιστοιχεί στον άγνωστο γονέα)
    try:
        if int(id) == 0:
            update_status("Το ID 0 είναι δεσμευμένο από το πρόγραμμα, δοκιμάστε άλλο ID!")
            return
        elif int(id) in get_IDs(buffer): # Το άτομο υπάρχει ήδη, επεξεργασία;
            replacing = tk.messagebox.askyesno(title="Αντικατάσταση;", message="Το ID:"+ id +" αντιστοιχεί στον "+ buffer.split("\n")[int(id)].split(",")[1] +"! Μπορεί να γίνει αντικατάσταση των βασικών στοιχείων εκτός από τα ID του πατέρα - μητέρας και το φύλο. Αν θέλετε να αλλάξετε τα προηγούμενα στοιχεία, τότε πρέπει να δημιουργήσετε νέο άτομο και να διαγράψετε το υπάρχων. Να γίνει αντικατάσταση;")
            update_status("Υπάρχει ήδη άτομο με αυτό το ID!")
            if not replacing:
                return
    except:
        update_status("Το ID πρέπει να είναι ακέραιος θετικός αριθμός.")
        return

    # Έλεγχος 2: Αν δώθηκε ονομασία και είναι με λατινικούς χαρακτήρες
    if name == "" or name.isascii() == False:
        update_status("Εισάγετε ονομασία του ατόμου με λατινικούς χαρακτήρες.")
        return
    if (re.search(r'\d', name)):
        update_status("Το όνομα δεν μπορεί να περιέχει νούμερα!")
        return

    # Έλεγχος 3: Μετατροπή και έλεγχος birth και death σε date_format και σύγκριση αν death > birth
    if death: # Δώθηκε ημερομηνία Θανάτου
        try:
            if dt.date(int(death.split("/")[2] if len(death.split("/")[2]) == 4 else ''),
                       int(death.split("/")[1] if len(death.split("/")[1]) == 2 else ''),
                       int(death.split("/")[0] if len(death.split("/")[0]) == 2 else '')) <= dt.date(
                    int(birth.split("/")[2] if len(birth.split("/")[2]) == 4 else ''),
                    int(birth.split("/")[1] if len(birth.split("/")[1]) == 2 else ''),
                    int(birth.split("/")[0] if len(birth.split("/")[0]) == 2 else '')):
                update_status("Η ημερομηνία γέννησης πρέπει να είναι μικρότερη της ημερομηνίας θανάτου.")
                return
        except:
            update_status('Οι ημερομηνίες πρέπει να είναι της μορφης "dd/mm/yyyy"!')
            return
    else: # Δεν δώθηκε ημερομηνία Θανάτου
        try:
            dt.date(int(birth.split("/")[2] if len(birth.split("/")[2]) == 4 else ''),
                    int(birth.split("/")[1] if len(birth.split("/")[1]) == 2 else ''),
                    int(birth.split("/")[0] if len(birth.split("/")[0]) == 2 else ''))
        except:
            update_status('Η ημερομηνία γέννησης πρέπει να είναι της μορφής "dd/mm/yyyy"!')
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

    # Έλεγχος 7: Εάν δωθεί ημερομηνία μεταγενέστερη της σημερινής
    if dt.date(int(birth.split("/")[2]),int(birth.split("/")[1]),int(birth.split("/")[0])) > dt.date( dt.datetime.now().year, dt.datetime.now().month, dt.datetime.now().day ):
        update_status("Δώσατε μεταγενέστερη ημερομηνία από την σημερινή.")
        return

    # Έλεγχος 8: Εάν ο χρήστης δώσει μόνο όνομα ή επίθετο.
    try:
        if (name.split(" ")[0] == "" or name.split(" ")[1] == ""):
            update_status("Δεν έχετε εισάγει σωστά το ονοματεπώνυμο!")
            return
    except:
        update_status("Δεν έχετε εισάγει σωστά το ονοματεπώνυμο!")
        return

    # Αντικατάσταση Χρήστη
    if replacing:
        data = pd.read_csv(StringIO(buffer), index_col=0)
        data.loc[int(id), "Name"] = name
        data.loc[int(id), "Birth"] = birth
        data.loc[int(id), "Death"] = death
        data.loc[int(id), "Description"] = desc
        buffer = data.to_csv(line_terminator="\n")
    # Εισαγωγή Χρήστη
    else:
        buffer += id+","+name+","+birth+","+death+","+sex+","+f_ID+","+m_ID+","+desc+"\n"
    subwindow.destroy() # Καταστρέφουμε το υποπαράθυρο
    update_status("Προστέθηκε ένα άτομο!")
    return on_view()


def valid(id_1, id_2):
    ''' Συνάρτηση που δέχεται 2 ID (πατέρα, μητέρα) και ελέγχει αν είναι ΟΚ η γέννηση παιδιού. '''
    if id_1 != 0 and id_2 != 0: # Εφόσον υπάρχουν και πατέρας και μητέρα

        # Δεδομένα σε λίστα: [ID,Name,Birth,Death,Sex,Father,Mother,Description]
        # Γονιών
        parent1 = buffer.split("\n")[id_1].split(",")
        parent2 = buffer.split("\n")[id_2].split(",")

        # Παππούδων
        gparent1 = [] # Λίστα με γονείς πρώτου ID
        gparent1_1 = buffer.split("\n")[int(parent1[5])].split(",")

        if gparent1_1[0].isnumeric(): gparent1.append(gparent1_1[0])
        gparent1_2 = buffer.split("\n")[int(parent1[6])].split(",")
        if gparent1_2[0].isnumeric(): gparent1.append(gparent1_2[0])

        gparent2 = [] # Λίστα με γονείς δεύτερου ID
        gparent2_1 = buffer.split("\n")[int(parent2[5])].split(",")
        if gparent2_1[0].isnumeric(): gparent2.append(gparent2_1[0])
        gparent2_2 = buffer.split("\n")[int(parent2[6])].split(",")
        if gparent2_2[0].isnumeric(): gparent2.append(gparent2_2[0])

        # Προπαππούδων
        ggparent1 = [] # Λίστα με παππούδες πρώτου ID
        for grandparent in gparent1:
            try:
                if int(buffer.split("\n")[int(grandparent)].split(",")[5]) != 0:
                    ggparent1.append( buffer.split("\n")[int(grandparent)].split(",")[5] )
            except:
                pass
            try:
                if int(buffer.split("\n")[int(grandparent)].split(",")[6]) != 0:
                    ggparent1.append( buffer.split("\n")[int(grandparent)].split(",")[6] )
            except:
                pass

        ggparent2 = [] # Λίστα με παππούδες δεύτερου ID
        for grandparent in gparent2:
            try:
                if int(buffer.split("\n")[int(grandparent)].split(",")[5]) != 0:
                    ggparent2.append( buffer.split("\n")[int(grandparent)].split(",")[5] )
            except:
                pass
            try:
                if int(buffer.split("\n")[int(grandparent)].split(",")[6]) != 0:
                    ggparent2.append( buffer.split("\n")[int(grandparent)].split(",")[6] )
            except:
                pass

        # Προπροπαππούδων
        gggparent1 = [] # Λίστα με προπαππούδες πρώτου ID
        for grandgrandparent in ggparent1:
            try:
                if int(buffer.split("\n")[int(grandgrandparent)].split(",")[5]) != 0:
                    gggparent1.append( buffer.split("\n")[int(grandgrandparent)].split(",")[5] )
            except:
                pass
            try:
                if int(buffer.split("\n")[int(grandgrandparent)].split(",")[6]) != 0:
                    gggparent1.append( buffer.split("\n")[int(grandgrandparent)].split(",")[6] )
            except:
                pass

        gggparent2 = [] # Λίστα με προπαππούδες δεύτερου ID
        for grandgrandparent in ggparent2:
            try:
                if int(buffer.split("\n")[int(grandgrandparent)].split(",")[5]) != 0:
                    gggparent2.append( buffer.split("\n")[int(grandgrandparent)].split(",")[5] )
            except:
                pass
            try:
                if int(buffer.split("\n")[int(grandgrandparent)].split(",")[6]) != 0:
                    gggparent2.append( buffer.split("\n")[int(grandgrandparent)].split(",")[6] )
            except:
                pass

        # Έλεγχος αν τα IDs είναι διαφορετικού Sex
        if parent1[4] == parent2[4]:
            update_status("Οι γονείς πρέπει να είναι διαφορετικού φύλου!")
            return False

        # Έλεγχος αν τα IDs έχουν σχέση παιδιού-γονέα
        if parent2[0] in gparent1: # Ένας από τους γονείς του id_1 είναι το ζεύγος του
            update_status("Δεν μπορεί γονέας να κάνει παιδί με το παιδί του!")
            return False
        if parent1[0] in gparent2: # Ένας από τους γονείς του id_2 είναι το ζεύγος του
            update_status("Δεν μπορεί γονέας να κάνει παιδί με το παιδί του!")
            return False

        # Έλεγχος για το αν θειος ζευγαρώσει με ανηψιά.
        for grandparent in ggparent1:
            if grandparent in gggparent2:
                update_status("Δεν μπορεί να ζευγαρώσει θείος με ανηψιά!")
                return False

        # Έλεγχος για το αν θεια ζευγαρώσει με ανηψιό.
        for grandparent in ggparent2:
            if grandparent in gggparent1:
                update_status("Δεν μπορεί να ζευγαρώσει θεία με ανηψιό!")
                return False

        # Έλεγχος αν τα IDs είναι αδέρφια
        for grandparent in gparent1:
            if grandparent in gparent2:
                update_status("Οι γονείς του ατόμου δεν μπορούν να είναι αδέρφια!")
                return False

        # Έλεγχος αν τα IDs είναι ξαδέρφια
        for grandparent in ggparent1:
            if grandparent in ggparent2:
                update_status("Οι γονείς του ατόμου δεν μπορούν να είναι ξαδέρφια!")
                return False

        # Έλεγχος αν τα IDs είναι δεύτερα ξαδέρφια
        for grandparent in gggparent1:
            if grandparent in gggparent2:
                update_status("Οι γονείς του ατόμου δεν μπορούν να είναι δεύτερα ξαδέρφια!")
                return False

    # Όλες οι σχέσεις ΟΚ
    return True


def update_status(txt):
    ''' Ανανεώνει το μήνυμα κατάστασης στην κάτω μπάρα της εφαρμογής. '''
    status_var.set(txt)


def on_delete():
    ''' Συνάρτηση που τρέχει όταν πατηθεί το κουμπί Διαγραφή στο interface της βασικής εφαρμογής. '''
    global subwindow
    # Δεν επιτρέπουμε την δημιουργία πολλαπλών υποπαραθύρων
    if subwindow == None or not tk.Toplevel.winfo_exists(subwindow):
        # Δημιουργία υποπαραθύρου και ορισμός των ιδιοτήτων του
        subwindow = tk.Toplevel(root)
        subwindow.title("GeneApp - Genealogy Tree Application")
        subwindow.columnconfigure(0, weight=1)
        subwindow.rowconfigure(0, weight=1)
        subwindow.geometry("240x100+750+500")
        subwindow.iconbitmap('favicon.ico')
        # Δημιουργία ενός frame wrapper μέσα στο υποπαράθυρο
        wrapper = ttk.Frame(subwindow)
        ttk.Label(wrapper, text="ID", font=("Arial 12"), foreground="#151515", background="#ddd").grid(row=0,column=0, columnspan=4, sticky=tk.W + tk.E)
        ID = tk.StringVar()
        ttk.Entry(wrapper, textvariable=ID).grid(row=0, column=4, columnspan=6, padx=8, pady=4)
        ttk.Button(wrapper, text="Διαγραφή", command=lambda: on_delete_confirm( str(ID.get())) ).grid(row=1)
        wrapper.grid(padx=14, pady=14)

        update_status("Διαγραφή ατόμου...")


def on_delete_confirm(ID):
    ''' Συνάρτηση που τρέχει όταν πατηθεί το "Διαγραφή" στο παράθυρο της Διαγραφής. '''
    global buffer

    try: # Έλεγχος ότι ID είναι θετικός ακέραιος, διάφορος του 0 και υπάρχει στη λίστα με τα διαθέσιμα IDs.
        if int(ID) > 0 and int(ID) in get_IDs(buffer):
            update_status("Το άτομο, που αντιστοιχεί στο ID προς διαγραφή, βρέθηκε.")
            sure = tk.messagebox.askyesno(title="Είστε σίγουρος για τη διαγραφή;", message="ΠΡΟΣΟΧΗ: Η διαγραφή του "+ buffer.split("\n")[int(ID)].split(",")[1] +" με ID:"+ ID +" θα διαγράψει και όλα τα άτομα-απογόνους που σχετίζονται με αυτόν. Θέλετε να συνεχίσετε;")
            if not sure: return
        else:
            update_status("Το ID προς διαγραφή δεν υπάρχει.")
            return
    except:
        update_status("Το ID προς διαγραφή δεν είναι έγκυρος αριθμός.")
        return
    
    # Έχουμε έγκυρο ID και επιβεβαίωση χρήστη
    to_delete = [ID] # Λίστα με ID προς διαγραφή (IDs -> str)
    for person in to_delete: # Βρόγχος που τρέχει για κάθε ID ατόμου προς διαγραφή
        for record in buffer.split("\n")[:-1]: # Για κάθε σειρά του Buffer (εκτός απ'την τελευταία που είναι κενή)
            if str(record.split(",")[5]) == person or str(record.split(",")[6]) == person: # Αν το άτομο έχει για ID πατέρα ή μητέρας το ID ατόμου προς διαγραφή
                to_delete.append(str(record.split(",")[0])) # Προσθήκη του ID του ατόμου στην λίστα
    # Διαγραφή Εγγραφών από τον buffer
    for person in to_delete:
        for record in buffer.split("\n")[:-1]:
            if str(record.split(",")[0]) == str(person):
                buffer = buffer.replace(record+"\n", "")
    update_status("Το άτομο διαγράφθηκε επιτυχώς!")
    subwindow.destroy()
    return on_view()


def get_ID():
    ''' Συνάρτηση που βρίσκει το αμέσως επόμενο διαθέσιμο ID. '''
    try:
        # Παίρνουμε όλα τα ID από την get_IDs, τα σορτάρουμε, διαλέγουμε το τελευταίο (μεγαλύτερο), προσθέτουμε +1, επιστρέφουμε την τιμή
        return int(sorted(get_IDs(buffer))[-1]+1)
    except:
        # Το return στο try πρέπει να δώσει στη χειρότερη περίπτωση ID=1
        # διότι το get_IDs επιστρέφει στην χειρότερη περίπτωση [0]. Οπότε απλά βάζουμε pass.
        pass


def get_IDs(buffer):
    ''' Συνάρτηση που δέχεται το String του Buffer και γυρνάει όλα τα IDs σε μια λίστα (+ το 0 το οποίο αντιστοιχεί στον άγνωστο γονέα). '''
    IDs = [0]
    try: # Το try χρειάζεται σε περίπτωση που ο Buffer έχει 1 row με μόνο τα headers (άρα ID != int)
        [IDs.append(int(record.split(",")[0])) for record in buffer.split("\n")[1:-1]] #[1:-1] γιατί το πρώτο στοιχείο είναι το "ID" και το τελευταίο το κενό (\n)
    except:
        pass
    return IDs # Η συνάρτηση γυρνάει σίγουρα λίστα με έστω ένα στοιχείο: [0]


def on_unload():
    global buffer
    # Reset the buffer
    buffer = "ID,Name,Birth,Death,Sex,Father,Mother,Description\n"
    update_status("Επιτυχής εκκάθαριση δεδομένων.")


def on_view():
    ''' Συνάρτηση που τρέχει όταν ο χρήστης πατήσει το κουμπί της προβολής δέντρου. '''
    # Δεν επιτρέπουμε την δημιουργία πολλαπλών γράφων
    plt.close() # Κλείνουμε τον γράφο
    global T
    T.clear() # Καθαρίζουμε τον γράφο για να τον ξανασχεδιάσουμε

    data = pd.read_csv(StringIO(buffer))
    data["Death"]=data["Death"].astype(str)

    # Καθάρισμα όλων των λεξικών
    livingMales.clear()
    deadMales.clear()
    livingFemales.clear()
    deadFemales.clear()

    # Ενημέρωση Χρήστη
    update_status("Προβολή γράφου...")

    # Προσθήκη Κορυφών και δημιουργία λιστών
    for person in data.index:
        newNode = [str(data.loc[person, "ID"]), data.loc[person, "Name"]]
        if data.loc[person, "Sex"] == 1:
            if data.loc[person, "Death"]=="nan":
                livingMales.update({newNode[0]:newNode[1]})
            else:
                deadMales.update({newNode[0]:newNode[1]})
        else:
            if data.loc[person, "Death"]=="nan":
                livingFemales.update({newNode[0]:newNode[1]})
            else:
                deadFemales.update({newNode[0]:newNode[1]})
        T.add_node(newNode[1])

    # Προσθήκη Ακμών
    for person in data.index:
        if data.loc[person, "Father"] != 0:
            personsFatherNumber = data.loc[person, "Father"]
            personsFather = data.loc[data['ID'] == personsFatherNumber,"Name"].values[0]
            v = personsFather
            u = data.loc[person, "Name"]
            T.add_edge(v, u)
        if data.loc[person, "Mother"] != 0:
            personsMotherNumber = data.loc[person, "Mother"]
            personsMother = data.loc[data['ID'] == personsMotherNumber,"Name"].values[0]
            v = personsMother
            u = data.loc[person, "Name"]
            T.add_edge(v, u)

    # Σχεδίαση Γράφου
    figure = plt.figure('GeneApp')
    figure.suptitle('Το Γενεαλογικό μου Δέντρο', fontsize=11,fontweight='bold')
    pos = graphviz_layout(T, prog="dot")

    nx.draw_networkx_nodes(T, pos, nodelist=[value for value in livingMales.values()], node_size=120, node_color="#2196f3", alpha = 1.0, margins=0.1)
    nx.draw_networkx_nodes(T, pos, nodelist=[value for value in deadMales.values()], node_size=120, node_color="#2196f3", alpha = 0.35, margins=0.1)
    nx.draw_networkx_nodes(T, pos, nodelist=[value for value in livingFemales.values()], node_size=120, node_color="#f06292", alpha = 1.0, margins=0.1)
    nx.draw_networkx_nodes(T, pos, nodelist=[value for value in deadFemales.values()], node_size=120, node_color="#f06292", alpha = 0.35, margins=0.1)

    nx.draw_networkx_labels(T, pos, labels = {value: key+") "+value for key,value in livingMales.items()}, alpha = 1.0, verticalalignment="top", font_size=10)
    nx.draw_networkx_labels(T, pos, labels = {value: key+") "+value for key,value in deadMales.items()}, alpha = 0.35, verticalalignment="top", font_size=10)
    nx.draw_networkx_labels(T, pos, labels = {value: key+") "+value for key,value in livingFemales.items()}, alpha = 1.0, verticalalignment="top", font_size=10)
    nx.draw_networkx_labels(T, pos, labels = {value: key+") "+value for key,value in deadFemales.items()}, alpha = 0.35, verticalalignment="top", font_size=10)

    nx.draw_networkx_edges(T, pos)
    plt.show()
    update_status("")


create_interface()
