# Genealogy Tree
Python Project Γενεαλογικού Δέντρου για το μάθημα ΠΛΗΠΡΟ: Προγραμματισμός.

## To Do List {#to-do}
- [ ] GUI Structure
- [ ] GUI Functionality
- [ ] Main Classes
- [ ] Class Functions
- [ ] Standalone Functions

### GUI Structure (T-Kinter) {#gui}
Main Container
  -- Button: "Insert Person"
    -- Form: ID, First, Last, Birth, Description, Family Connections
      -- (ID Exists) Container: "Replace Info?"
      -- (ID Not Exists) Container: "Person Created."
  -- Button: "Remove Person"
    -- Form: ID
      -- (ID Exists) Container: "Person with ID Removed."
      -- (ID Not Exists) Container: "Person not found."
  -- View Graph Tree
  -- Save
    -- Open Explorer to select saving folder/file.
  -- Load
    -- Open Explorer to load file.

### Classes & Functions {#functions}