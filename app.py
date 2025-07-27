import os
import time
import re
import sqlite3
import bcrypt
import random
from getpass import getpass
from termcolor import cprint

from user import User

DB_FILE = 'finance.db'

main_banner = """
####################
#   Skynet Bank    #
####################
"""

main_menu = """
[R] Register
[L] Login
[Q] Quit
"""

register_banner = """
###############################
#   Skynet Bank -  Register   #
###############################
"""

login_banner = """
############################
#   Skynet Bank -  Login   #
############################
"""

app_banner = """
###############################
#   Skynet Bank -  Dashboard  #
###############################
"""

app_menu = """
[D] Deposit
[W] Withdraw
[T] Transfer
[AD] Account Details
[CB] Check Balance
[TH] Transaction History
[X] Logout
"""


global message
message = ("", "")

def _wait():
    process = ""
    for _ in range(11):
        process += "#"
        cprint(f"Loading: {process}", "green", end="\r")
        time.sleep(0.5)
        
        
def _generate_account_number():
    while True:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            account_number = str(random.randint(10000000, 99999999))
            if not cursor.execute("SELECT 1 FROM users WHERE account_number = ?", (account_number,)).fetchone():
                return account_number


def _alert(mess: tuple[str, str]):
    if mess:
            if mess[1] == "suc": # type: ignore
                cprint(mess[0], "white", "on_green")
            elif mess[1] == "err":
                cprint(mess[0], "white", "on_red")
            else:
                cprint(mess[0], "white")


def _deposite(acc_holder: User):
    global message
    message = ("", "")
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        _alert(message)
        print("""
###############################
#   Skynet Bank -  Deposit   #
###############################
              """)
        while True:
            deposit_amount = input("Enter deposit amount (minimum 1000): ").strip()
            if not deposit_amount:
                cprint("Deposit amount is required", "red")
                continue
            if not deposit_amount.isdigit() or int(deposit_amount) < 1000:
                cprint("Invalid deposit amount. Please enter a valid amount (minimum 1000).", "red")
                continue
            break

        acc_holder.deposit(float(deposit_amount))
        message = (f"Deposit of {deposit_amount} successful!", "suc")
        _wait()
        break
    
    
def _withdraw(acc_holder: User):
    global message
    message = ("", "")
    os.system('clear' if os.name == 'posix' else 'cls')
    _alert(message)
    print("""
###############################
#   Skynet Bank -  Withdraw  #
###############################
            """)
    
    while True:
        withdraw_amount = input("Enter withdrawal amount: ").strip()
        if not withdraw_amount:
            cprint("Withdrawal amount is required", "red")
            continue
        
        if not withdraw_amount.isdigit():
            cprint("Invalid withdrawal amount.", "red")
            continue
        
        if float(withdraw_amount) > acc_holder.balance:
            cprint("Insufficient funds", "red")
            continue
        break

    acc_holder.withdraw(float(withdraw_amount))
    message = (f"Withdrawal of ${withdraw_amount} successful!", "suc")
    _wait()
        
        
def _transfer(acc_holder: User):
    global message
    message = ("", "")
    os.system('clear' if os.name == 'posix' else 'cls')
    _alert(message)
    print("""
##############################
#   Skynet Bank -  Transfer  #
##############################
            """)
    while True:
        reciver_account = input("Enter receiver account number: ")
        if not reciver_account:
            cprint("Receiver account number is required", "red")
            continue
        if reciver_account == acc_holder.account_number:
            cprint("You cannot transfer to your own account", "red")
            continue
        break

    while True:
        transfer_amount = input("Enter transfer amount: ").strip()
        if not transfer_amount:
            cprint("Transfer amount is required", "red")
            continue
        if not transfer_amount.isdigit():
            cprint("Invalid transfer amount. Please enter a valid amount.", "red")
            continue
        if float(transfer_amount) > acc_holder.balance:
            cprint("Insufficient funds", "red")
            continue
        break
    _wait()
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        to_acc = cursor.execute("SELECT True FROM users WHERE account_number = ?", (reciver_account,)).fetchone()
        
        if to_acc:
            acc_holder.transfer(reciver_account, float(transfer_amount))
            message = (f"Transfer of ${transfer_amount} to {reciver_account} successful!", "suc")
        else:
            message = ("Invalid Account number!", "err")


def main(acc_holder: User): # type: ignore
    global message
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        _alert(message)
        print(app_banner)
        print(app_menu)
        
        option = str(input("Choose an option: ")).strip().upper()
        
        if option == "D":
            _deposite(acc_holder)
        elif option == "W":
            _withdraw(acc_holder)
        elif option == "T":
            _transfer(acc_holder)
        elif option == "AD":
            message = (f"{acc_holder.get_user_details}", "-")
        elif option == "CB":
            message = (f"{acc_holder.get_user_balance}", "-")
        elif option == "TH":
            transaction_history = acc_holder.get_transaction_history
            if transaction_history:
                message = (transaction_history, "-")
        elif option == "X":
            message = ("Logged out successfully!", "suc")
            _wait()
            break
        else:
            message = ("Invalid option. Please try again.", "err")
            continue


def sign_up():
    global message
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        _alert(message)
        print(register_banner)
        name_pattern = r"^[a-zA-Z\s]{4,255}$"
        username_pattern = r"^[a-zA-Z0-9_]{3,20}$"
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,30}$"

        # Name input
        while True:
            first_name = input("Enter your first name: ").strip()
            if not first_name:
                cprint("First name is required", "red")
                continue
            break
        while True:
            last_name = input("Enter your last name: ").strip()
            if not last_name:
                cprint("Last name is required", "red")
                continue
            break
        full_name = f"{first_name} {last_name}"
        if not re.match(name_pattern, full_name):
            cprint("Full name must be between 4 and 255 characters and contain only letters and spaces.", "red")
            continue

        # Username input
        while True:
            username = input("Enter your username (Letters, numbers, underscores only): ").strip()
            if not username:
                cprint("Username is required", "red")
                continue
            if not re.match(username_pattern, username):
                cprint("Username must be between 3 and 20 characters and contain only letters, numbers, and underscores.", "red")
                continue
            break

        # Deposit input
        while True:
            deposit_input = input("Enter your initial deposit (minimum $2000): ").strip()
            if not deposit_input:
                cprint("Initial deposit is required", "red")
                continue
            if not deposit_input.isdigit():
                cprint("Initial deposit must be a numeric value and at least $2000.", "red")
                continue
            initial_deposit = float(deposit_input)
            if initial_deposit < 2000:
                cprint("Initial deposit must be at least $2000.", "red")
                continue
            if initial_deposit < 0:
                cprint("Initial deposit cannot be negative.", "red")
                continue
            break

        # Password input
        while True:
            password = getpass("Enter your password: ").strip()
            if not password:
                print("Password is required")
                continue
            if not re.match(password_pattern, password):
                print("Password must be between 8 and 30 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character.")
                continue
            confirm_password = getpass("Confirm your password: ").strip()
            if not confirm_password:
                print("Confirm Password is required")
                continue
            if password != confirm_password:
                print("Passwords don't match")
                continue
            break

        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        account_number = _generate_account_number()

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (fullname, username, password, balance, account_number) VALUES (?, ?, ?, ?, ?)
                """, (full_name, username, hash_password, initial_deposit, account_number))
            except sqlite3.IntegrityError as e:
                if "username" in str(e):
                    message = ("Username already exists", "err")
                    continue
            
            message = ("Sign up successful", "suc")
            _wait()
        break
    login()
    
    
def login():
    global message
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        _alert(message)
        print(login_banner)
        while True:
            username = input("Enter your username: ").strip()
            if not username:
                cprint("Username is required", "red")
                continue
            break

        while True:
            password = getpass("Enter your password: ").strip()
            if not password:
                cprint("Password is required", "red")
                continue
            _wait()
            break
    
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            
            user = cursor.execute("SELECT id, fullname, balance, account_number, username, password FROM users WHERE username = ?", (username,)).fetchone()
            
            if user:
                _id, full_name, balance, account_number, _username, hash_password = user
                if _username == username and bcrypt.checkpw(password.encode("utf-8"), hash_password):
                    message = f"Login successful! Welcome back {full_name}", "suc"
                    user_instance = User(_id=_id, full_name=full_name, username=_username, balance=balance, account_number=account_number)
                    main(user_instance)
                    break
                else:
                    message = "Username or Password is incorrect", "err"
            else:
                message = "Username or Password is incorrect", "err"


while True:
    os.system('clear' if os.name == 'posix' else 'cls')
    _alert(message)
    print(main_banner)
    print(main_menu)
    option = str(input("Choose an option: ")).strip().upper()
    
    if option == "R":
        _wait()
        sign_up()
    elif option == "L":
        _wait()
        login()
    elif option == "Q":
        print("Thank you for using Skynet Bank. Goodbye!")
        break
    else:
        message = ("Invalid option. Please try again.", "err")
        continue
    