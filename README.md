# Genealogy Tree
Python Project Γενεαλογικού Δέντρου για το μάθημα ΠΛΗΠΡΟ: Προγραμματισμός.

## To Do List
- [x] GUI Structure
- [x] GUI Linking
- [x] Standalone Functions

### GUI Structure (T-Kinter)
```
Main Container
  -- Button: "Εισαγωγή Ατόμου"
    -- Form: ID, Name, Birth, Death, Sex, Father, Mother, Description
      -- (Αν ID Υπάρχει) "Αντικατάσταση;"
      -- (ID δεν Υπάρχει) "Δημιουργήθηκε νέο άτομο."
  -- Button: "Διαγραφή Ατόμου"
    -- Form: ID
      -- (Αν ID Υπάρχει) "Διαγραφή του ατόμου και όλων των συνδέσεων του προς τα κάτω."
      -- (ID δεν υπάρχει) "Δεν βρέθηκε το άτομο."
  -- Button: "Προβολή Γράφου"
  -- Button: "Καθάρισμα Γράφου"
  -- Αποθήκευση
    -- Ανοίγει Explorer για επιλογή path, ελέγχει buffer και αποθηκεύει σε csv.
  -- Φόρτωση
    -- Ανοίγει Explorer για επιλογή file, ελέγχει αν .csv και τα headers και φορτώνει στον buffer.
```
