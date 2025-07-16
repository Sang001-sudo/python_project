import sqlite3

def db(db_name:str = 'finance.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print(f"Connected to database '{db_name}'")
    return cursor

def create_database():
    cursor = db('finance.db')

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
