# 📚Library Management System

A lightweight desktop application for managing a personal book collection, built with **Python**, **Tkinter**, and **SQLite**.

---

## Features

- **Add Books** — Store book records with Title, Author, Year, and ISBN
- **View All** — Display the entire book catalog in a scrollable table
- **Search** — Find books by any combination of Title, Author, Year, or ISBN
- **Update** — Edit details of an existing book entry
- **Delete** — Remove a book record (with confirmation prompt)
- **Input Validation** — Ensures Year and ISBN are valid numbers, and required fields are filled

## Tech Stack

| Layer     | Technology         |
|-----------|--------------------|
| Language  | Python 3           |
| GUI       | Tkinter (ttk)      |
| Database  | SQLite3            |

## Project Structure

```
Library Management System/
├── database.py          # Database class — CRUD operations via SQLite
├── library_frontend.py  # Tkinter GUI — user interface & event handlers
├── library.db           # SQLite database file (auto-created on first run)
└── README.md
```

## Getting Started

### Prerequisites

- **Python 3.6+** — [Download here](https://www.python.org/downloads/)
- Tkinter comes pre-installed with most Python distributions on Windows. No additional packages are required.

### Run the Application

```bash
python library_frontend.py
```

The application window will open with all existing books loaded automatically.

## Usage

1. **Add a book** — Fill in the Title, Author, Year, and ISBN fields, then click **Add Entry**.
2. **View all books** — Click **View All** to refresh the table with every record.
3. **Search** — Enter a value in one or more fields and click **Search Entry**.
4. **Update a book** — Select a row in the table, modify the fields, and click **Update Selected**.
5. **Delete a book** — Select a row and click **Delete Selected**. Confirm the prompt to remove it.
6. **Clear fields** — Click **Clear Fields** to reset all input boxes.

## Screenshots

| Input & Buttons | Book Table |
|---|---|
| Title, Author, Year, ISBN fields at the top | Scrollable Treeview with ID, Title, Author, Year, ISBN columns |

## License

This project is open-source and available for personal and educational use.
