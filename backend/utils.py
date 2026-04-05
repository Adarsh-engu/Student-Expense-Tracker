import sqlite3

def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db_connection()
    
    # 1. Create users table (Now strictly using username!)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL
        )
    ''')
    
    # 2. Create expenses table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database connected and tables initialized successfully!")

if __name__ == '__main__':
    init_db()