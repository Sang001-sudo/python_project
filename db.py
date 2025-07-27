import sqlite3

DB_FILE = 'finance.db'

def create_database():
   with sqlite3.connect(DB_FILE) as conn:
       cursor = conn.cursor()

       try:
           cursor.execute('''
               CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   fullname TEXT NOT NULL,
                   username TEXT NOT NULL UNIQUE,
                   account_number TEXT NOT NULL UNIQUE,
                   balance REAL NOT NULL,
                   password TEXT NOT NULL
               )
           ''')
           cursor.execute('''
               CREATE TABLE IF NOT EXISTS transactions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   amount REAL NOT NULL,
                   type TEXT NOT NULL,
                   date TEXT DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
               )
           ''')
           print("Table created or already exists.")
       except sqlite3.Error as e:
           print(f"Error creating users table: {e}")
           cursor.close()
           return
       finally:
           try:
               cursor.close()
           except Exception as e:
               print(e)
            



if __name__ == "__main__":
    create_database()
