import bcrypt
from db import db
import sqlite3

cursor = db()

class user:
    def __init__(self):
        self.id  # type: ignore
        self.full_name # type: ignore
        self.username # type: ignore
        self.balance # type: ignore
        self.account_number # type: ignore
        
        
    def register(self, full_name: str, username: str, password: str, initial_deposit: float):
        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            cursor.execute("""
                INSERT INTO users (full_name, username, password, initial_deposit) VALUES (?, ?, ?, ?)
            """, (full_name, username, hash_password, initial_deposit))
        except sqlite3.IntegrityError as e:
            e = str(e)
            if "full_name" in e:
                print(f"Name already exists: {e}")
            elif "username" in e:
                print(f"Username already exists: {e}")
        else:
            print("Sign up successful 🥳")
    
    
    def login(self, username: str, password: str):
        user_data = cursor.execute("SELECT fullname, balance, account_number, username, password FROM users WHERE username = ?", (username,)).fetchone()
        if user_data:
            full_name, balance, account_number, username, hash_passwd = user_data
            stored_password = hash_passwd
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                self.full_name = full_name
                self.balance = balance 
                self.account_number = account_number 
                self.username = username 
                print(f"Login successful! Welcome back {self.full_name}!")
            else:
                print("Incorrect username or password")
        else:
            print("Incorrect username or password")
    
    def deposit(self, username: str, amount: float):
        pass
    
    def withdraw(self, username: str, amount: float):
        pass
    
    def transfer(self, from_user: str, to_user: str, amount: float):
        pass
    
    @property
    def get_balance(self): # type: ignore
        return self.balance # type: ignore

    @property
    def get_user_details(self):
        return f"Fullname: {self.fullname}\nUsername: {self.username}\nAccount Number: {self.account_number}\nAccount Balance: ${self.balance}" # type: ignore
    
    @property
    def get_transaction_history(self):
        transaction = cursor.execute("SELECT transact.id, transact.type, transact.amount, transact.date FROM users user JOIN transactions transact ON user.id = transact.user_id WHERE user.username = ?",(self.username,)).fetchall() # type: ignore
        return transaction