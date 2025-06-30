# database.py

import sqlite3

# Create/connect to the database
def connect_db():
    return sqlite3.connect("csv_analyzer.db")

# Create table if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            uploaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rows INTEGER,
            columns INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Insert metadata
def insert_metadata(filename, rows, columns):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO file_metadata (filename, rows, columns)
        VALUES (?, ?, ?)
    ''', (filename, rows, columns))
    conn.commit()
    conn.close()

# Fetch recent uploads (optional for display)
def get_metadata():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT filename, uploaded_on, rows, columns
        FROM file_metadata
        ORDER BY uploaded_on DESC
        LIMIT 10
    ''')
    data = cursor.fetchall()
    conn.close()
    return data
