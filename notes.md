# Bank Project Notes

## Git & GitHub

Create a new GitHub repo and push local code:
```bash
gh repo create Bank --private --source=. --push
```

Add a remote and push for the first time:
```bash
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin master
```

The `-u` flag sets the upstream so future `git push` commands work without specifying the remote.

---

## PostgreSQL with psycopg2

Install the library (inside your virtual environment):
```bash
pip install psycopg2-binary python-dotenv
```

Basic connection and query:
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="your_db",
    user="your_user",
    password="your_password"
)

cursor = conn.cursor()
cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", ("Zach", 1000))
conn.commit()

cursor.execute("SELECT * FROM accounts")
rows = cursor.fetchall()
```

- Always call `conn.commit()` after inserts/updates
- Use `%s` placeholders instead of f-strings to avoid SQL injection
- `fetchall()` returns a list of tuples, `fetchone()` returns a single row

---

## Hiding Credentials with .env

Install python-dotenv:
```bash
pip install python-dotenv
```

Create a `.env` file in your project root:
```
DB_HOST=localhost
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
```

Add `.env` and `venv` to `.gitignore`:
```bash
echo ".env" >> .gitignore
echo "venv" >> .gitignore
```

Load in Python:
```python
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    options="-c search_path=bank"
)
```

`options="-c search_path=bank"` tells PostgreSQL to use the `bank` schema by default.

---

## Virtual Environment (Arch Linux / Fish Shell)

Arch Linux blocks system-wide pip installs, so use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate.fish   # fish shell specific
```

Note: fish shell uses `activate.fish`, not `activate`.

---

## PostgreSQL Schema & Tables

Connect with psql and create a schema:
```sql
CREATE SCHEMA bank;
```

Set search path so you don't have to prefix every table:
```sql
SET search_path TO bank;
```

Create tables (order matters — referenced tables must be created first):
```sql
CREATE TABLE bank.users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL
);

CREATE TABLE bank.accounts (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES bank.users(id),
    name VARCHAR(255) NOT NULL,
    balance DECIMAL(10,2) DEFAULT 0.00
);
```

- `SERIAL` auto-generates IDs on insert
- `DECIMAL(10,2)` — 10 total digits, 2 after the decimal (good for money)
- `REFERENCES bank.users(id)` is the foreign key linking accounts to users

Add a column to an existing table:
```sql
ALTER TABLE bank.accounts ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
```

Insert data (users first, then accounts):
```sql
INSERT INTO users (first_name, last_name) VALUES ('Zach', 'Kenney');
INSERT INTO accounts (user_id, name, balance) VALUES (1, 'Checking', 500.00);
```

Join tables:
```sql
SELECT * FROM users
JOIN accounts ON users.id = accounts.user_id;
```

---

## Testing the DB Connection

```python
def connectionVerify():
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    print(cursor.fetchone())

connectionVerify()
```
