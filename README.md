# Genealogy Tree
Python Project Γενεαλογικού Δέντρου για το μάθημα ΠΛΗΠΡΟ: Προγραμματισμός.

## To Do List
- [ ] GUI Structure
- [ ] GUI Functionality
- [ ] Main Classes
- [ ] Class Functions
- [ ] Standalone Functions

### GUI Structure (T-Kinter)
```
Main Container<br>
  -- Button: "Insert Person"<br>
    -- Form: ID, First, Last, Birth, Description, Family Connections<br>
      -- (ID Exists) Container: "Replace Info?"<br>
      -- (ID Not Exists) Container: "Person Created."<br>
  -- Button: "Remove Person"<br>
    -- Form: ID<br>
      -- (ID Exists) Container: "Person with ID Removed."<br>
      -- (ID Not Exists) Container: "Person not found."<br>
  -- View Graph Tree<br>
  -- Save<br>
    -- Open Explorer to select saving folder/file.<br>
  -- Load<br>
    -- Open Explorer to load file.<br>
```

### Classes & Functions