# Library Management System

A desktop Library Management System built with Python, Tkinter and SQLite.

## Features
- Dashboard with library statistics
- Add, edit, delete and search books
- Track multiple copies and available copies
- Add, edit, delete and search borrowers
- Issue books with configurable loan period
- Return books
- Automatic overdue fine calculation
- Reports for overdue books, issued books and all transactions
- Works offline using SQLite

## Requirements
- Python 3.10+ (developed/tested for Python 3.12)
- Tkinter

On Ubuntu/Linux Mint:
```bash
sudo apt install python3-tk
```

## Run
From the project folder:
```bash
python3 main.py
```

The database is automatically created at:
`database/library.db`

## Optional demo data
Run:
```bash
python3 -c "from database.db import initialize_database, seed_demo_data; initialize_database(); seed_demo_data()"
```

Then start the application.

## Fine calculation
The current implementation uses UGX 500 per overdue day. This can be changed in `database/db.py`.

## Notes
The application is intentionally single-user/offline, matching the project proposal's stated scope and limitation.
