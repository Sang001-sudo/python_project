import bcrypt # type: ignore
from db import db

cursor = db()

class user:
    def __init__(self):
        self.id  # type: ignore
        self.full_name # type: ignore
        self.username # type: ignore
        self.balance # type: ignore
        self.account_number # type: ignore
        
        
    def register(self, full_name: str, username: str, password: str, initial_deposit: float):
        pass
    
    def login(self, username: str, password: str):
        pass
    
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