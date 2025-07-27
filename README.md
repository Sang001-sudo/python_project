# Skynet Bank

Skynet Bank is a simple command-line banking application built with Python and SQLite. It allows users to register, log in, deposit, withdraw, transfer funds, and view transaction history.

## Features

- User registration and login with secure password hashing (bcrypt)
- Deposit, withdraw, and transfer funds between accounts
- View account details and balance
- Transaction history display
- Input validation and error handling
- Colorful terminal output (termcolor)
- Tabular data display (tabulate)

## Requirements

- Python 3.12+
- [bcrypt](https://pypi.org/project/bcrypt/)
- [tabulate](https://pypi.org/project/tabulate/)
- [termcolor](https://pypi.org/project/termcolor/)

Install dependencies:

```sh
pip install -r requirements.txt

```

## Usage
- Initialize the database (optional, runs automatically if not present):
```sh
python db.py
```

- Start the application:
```sh
python app.py
```


