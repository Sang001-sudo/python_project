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
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            try:
                new_balance = self.balance - amount
                cursor.execute("""
                    UPDATE users
                    SET balance = ?
                    WHERE id = ?;
                """, (new_balance, self.id))
                cursor.execute("""
                    INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)
                """, (self.id, "withdraw", amount))
                self.balance = new_balance
            except sqlite3.Error as e:
                print(f"Error: {e}")


    def transfer(self, to_account: str, amount: float):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            try:
                to_acc = cursor.execute("SELECT id, balance FROM users WHERE account_number = ?", (to_account,)).fetchone()
                if to_acc:
                    to_balance = to_acc[1] + amount
                    cursor.execute("""
                        UPDATE users
                        SET balance = ?
                        WHERE account_number = ?;
                    """, (to_balance, to_account))
                    
                    new_balance = self.balance - amount
                    cursor.execute("""
                        UPDATE users
                        SET balance = ?
                        WHERE id = ?;
                    """, (new_balance, self.id))
                    self.balance = new_balance
                    
                    cursor.execute("""
                        INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)
                    """, (self.id, f"transfer to {to_account}", amount))
                    cursor.execute("""
                        INSERT INTO transactions (user_id, type, amount) VALUES (?, ?, ?)
                    """, (to_acc[0], f"transfer from {self.account_number}", amount))
            except sqlite3.Error as e:
                print(f"Error: {e}")


    @property
    def get_user_details(self):
        return tabulate([[f"Fullname: {self.full_name}"],
                          [f"Username: {self.username}"],
                          [f"Account Number: {self.account_number}"]],
                         tablefmt="grid")
        
        
    @property
    def get_user_balance(self):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            self.balance = cursor.execute("SELECT balance FROM users WHERE username = ?", (self.username,)).fetchone()[0]
            return tabulate([[f"Account Balance: ${self.balance}"]],
                         tablefmt="grid")

    @property
    def get_transaction_history(self):
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            transaction = cursor.execute("SELECT transact.id, transact.type, transact.amount, transact.date FROM users user JOIN transactions transact ON user.id = transact.user_id WHERE user.username = ?",(self.username,)).fetchall() # type: ignore

        return tabulate(transaction, headers=["Transaction id", "Type", "Amount", "Date"], tablefmt="grid") if transaction else "No transactions found."