import tkinter as tk
from tkinter import ttk, messagebox
from database import Database  # Assuming database.py is unchanged

db = Database("library.db")

selected_item_id = None # To hold the ID of the book selected in the Treeview

def get_selected_row(event):
    """
    Handles item selection in the Treeview and populates the Entry fields.
    """
    global selected_item_id
    try:
        # Get the ID (item identifier) of the selected row in the Treeview
        selected_row_id = tree.focus()
        if not selected_row_id:
            return

        # Get the values associated with that item ID
        values = tree.item(selected_row_id, 'values')

        # The ID is the first value, but we need to ensure the selection is valid
        if values:
            selected_item_id = values[0]
            # Populate entry fields (Note: indices match the database columns)
            title_text.set(values[1])
            author_text.set(values[2])
            year_text.set(values[3])
            isbn_text.set(values[4])
        else:
            selected_item_id = None

    except IndexError:
        selected_item_id = None # Should not happen with Treeview, but safe
        pass

def clear_tree():
    """Clears all rows from the Treeview."""
    for item in tree.get_children():
        tree.delete(item)

def view_command():
    """Fetches and displays all books in the Treeview."""
    clear_tree()
    for row in db.view():
        tree.insert('', 'end', values=row)

def search_command():
    """Searches the database based on non-empty Entry fields."""
    clear_tree()
    try:
        # Use a tuple for search parameters, coercing year/isbn to appropriate types if provided
        year = int(year_text.get()) if year_text.get() else ""
        isbn = int(isbn_text.get()) if isbn_text.get() else ""
        
        rows = db.search(title_text.get(), author_text.get(), year, isbn)
        for row in rows:
            tree.insert('', 'end', values=row)
    except ValueError:
        messagebox.showerror("Input Error", "Year and ISBN must be valid numbers for searching.")


def add_command():
    """Adds a new book record and refreshes the view."""
    try:
        # Input validation
        title = title_text.get()
        author = author_text.get()
        year = int(year_text.get())
        isbn = int(isbn_text.get())
        
        if not title or not author:
             messagebox.showwarning("Input Missing", "Title and Author fields cannot be empty.")
             return

        db.insert(title, author, year, isbn)
        clear_entries()
        view_command() 
    except ValueError:
        messagebox.showerror("Input Error", "Year and ISBN must be valid numbers.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def delete_command():
    """Deletes the selected book record."""
    global selected_item_id
    if selected_item_id:
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected book?"):
            db.delete(selected_item_id)
            view_command()
            clear_entries()
            selected_item_id = None
    else:
        messagebox.showwarning("Selection Error", "Please select a book to delete.")

def update_command():
    """Updates the selected book record."""
    global selected_item_id
    if selected_item_id:
        try:
            db.update(
                selected_item_id, 
                title_text.get(), 
                author_text.get(), 
                int(year_text.get()), 
                int(isbn_text.get())
            )
            view_command()
            clear_entries()
            selected_item_id = None
        except ValueError:
            messagebox.showerror("Input Error", "Year and ISBN must be valid numbers for the update.")
    else:
        messagebox.showwarning("Selection Error", "Please select a book to update.")

def clear_entries():
    """Clears all text entry fields."""
    title_text.set("")
    author_text.set("")
    year_text.set("")
    isbn_text.set("")
    tree.selection_remove(tree.focus()) # Deselect the row

# --- GUI Setup ---
window = tk.Tk()
window.title("📚 Mini Library Manager")
# Setting the theme for ttk widgets
style = ttk.Style()
style.theme_use('clam') # 'clam', 'alt', 'default', 'classic' are options

# Frame for Entry fields (Input Area)
input_frame = ttk.Frame(window, padding="10")
input_frame.grid(row=0, column=0, columnspan=4, sticky='ew')

# Frame for Buttons
button_frame = ttk.Frame(window, padding="10")
button_frame.grid(row=1, column=0, columnspan=4, sticky='ew')

# Frame for Treeview (Output Area)
tree_frame = ttk.Frame(window, padding="10")
tree_frame.grid(row=2, column=0, columnspan=4, sticky='nsew')
window.grid_rowconfigure(2, weight=1) # Makes the list area expandable
window.grid_columnconfigure(0, weight=1) # Makes the list area expandable

# --- Input Area (Grid layout within input_frame) ---
ttk.Label(input_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
ttk.Label(input_frame, text="Author:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
ttk.Label(input_frame, text="Year:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
ttk.Label(input_frame, text="ISBN:").grid(row=1, column=2, padx=5, pady=5, sticky='w')

# Entry Fields
title_text = tk.StringVar()
ttk.Entry(input_frame, textvariable=title_text, width=30).grid(row=0, column=1, padx=5, pady=5, sticky='ew')

author_text = tk.StringVar()
ttk.Entry(input_frame, textvariable=author_text, width=30).grid(row=0, column=3, padx=5, pady=5, sticky='ew')

year_text = tk.StringVar()
ttk.Entry(input_frame, textvariable=year_text, width=15).grid(row=1, column=1, padx=5, pady=5, sticky='w')

isbn_text = tk.StringVar()
ttk.Entry(input_frame, textvariable=isbn_text, width=15).grid(row=1, column=3, padx=5, pady=5, sticky='w')

# Configure column weights for input_frame for better stretching
input_frame.grid_columnconfigure(1, weight=1)
input_frame.grid_columnconfigure(3, weight=1)

# --- Treeview (Output) ---
# Define columns for the Treeview
columns = ('id', 'title', 'author', 'year', 'isbn')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

# Set column headings and width
tree.heading('id', text='ID')
tree.heading('title', text='Title')
tree.heading('author', text='Author')
tree.heading('year', text='Year')
tree.heading('isbn', text='ISBN')

tree.column('id', width=50, stretch=tk.NO) # Don't stretch the ID column
tree.column('title', width=200, anchor=tk.W)
tree.column('author', width=150, anchor=tk.W)
tree.column('year', width=70, anchor=tk.CENTER)
tree.column('isbn', width=120, anchor=tk.CENTER)

tree.grid(row=0, column=0, sticky='nsew')
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

# Add Scrollbar
vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
vsb.grid(row=0, column=1, sticky='ns')
tree.configure(yscrollcommand=vsb.set)

# Bind the selection event
tree.bind('<<TreeviewSelect>>', get_selected_row)

# --- Buttons (Grid layout within button_frame) ---
ttk.Button(button_frame, text="View All", command=view_command).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Search Entry", command=search_command).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Add Entry", command=add_command).grid(row=0, column=2, padx=5, pady=5)
ttk.Button(button_frame, text="Update Selected", command=update_command).grid(row=0, column=3, padx=5, pady=5)
ttk.Button(button_frame, text="Delete Selected", command=delete_command).grid(row=0, column=4, padx=5, pady=5)
ttk.Button(button_frame, text="Clear Fields", command=clear_entries).grid(row=0, column=5, padx=5, pady=5)
ttk.Button(button_frame, text="Close", command=window.destroy).grid(row=0, column=6, padx=5, pady=5)

# Configure button_frame to center buttons
for i in range(7):
    button_frame.grid_columnconfigure(i, weight=1)

# Initial load
view_command()

# Run the Tkinter main loop
window.mainloop()