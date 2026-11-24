# Database Layer - SQL se baat karega
# C# me jaise ADO.NET / EF Core hota tha, waisa hi hai
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Taaki naam se data mile
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            naam TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            city TEXT,
            experience INTEGER,
            ctc INTEGER
        )
    """)
    # Pehli baar default user daal do
    try:
        conn.execute("INSERT INTO users (username, password, naam) VALUES (?, ?, ?)", ("amit", "12345", "Amit Kumar Tiwari"))
        conn.execute("INSERT INTO employees (name, city, experience, ctc) VALUES (?, ?, ?, ?)", ("Amit Kumar Tiwari", "New Delhi", 8, 15))
        conn.execute("INSERT INTO employees (name, city, experience, ctc) VALUES (?, ?, ?, ?)", ("【entity-Rahul Sharma¦canonical_name=Rahul Sharma】", "Lucknow", 2, 8))
    except:
        pass  # Agar pehle se hai to dobara mat daalo
    conn.commit()
    conn.close()
    print("Database Ready Hai!")

if __name__ == "__main__":
    init_db()