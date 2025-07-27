import sqlite3
from tabulate import tabulate


DB_FILE = 'finance.db'


class User:
    def __init__(self, _id:int, full_name:str, username:str, balance:float, account_number:str):
        self.id = _id
        self.full_name = full_name
        self.username = username
        self.balance = balance
        self.account_number = account_number


    def deposit(self, amount: float):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            try:
                new_balance = self.balance + amount
                cursor.execute("""
                    UPDATE users
                    SET balance = ?
                    WHERE id = ?;
                """, (new_balance, self.id))
                cursor.execute("""
                    INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)
                """, (self.id, "deposit", amount))
                self.balance = new_balance
            except Exception as e:
                print(f"Error: {e}")

    def withdraw(self, amount: float):
        if amount > self.balance:
            print("Insufficient funds")
            return
        self.balance -= amount
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)
            """, (self.id, "withdraw", amount))

    def transfer(self, from_user: str, to_user: str, amount: float):
        pass
    

    @property
    def get_user_details(self):
        return f"Fullname: {self.full_name}\nUsername: {self.username}\nAccount Number: {self.account_number}\nAccount Balance: ${self.balance}" # type: ignore
    
    @property
    def get_transaction_history(self):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            transaction = cursor.execute("SELECT transact.id, transact.type, transact.amount, transact.date FROM users user JOIN transactions transact ON user.id = transact.user_id WHERE user.username = ?",(self.username,)).fetchall() # type: ignore


        return tabulate(transaction, headers=["Transaction id", "Type", "Amount", "Date"], tablefmt="grid") if transaction else "No transactions found."