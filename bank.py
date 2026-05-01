from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def connectionVerify():
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    print(cursor.fetchone())

class createUser:
    def __init__(self):
        pass

    def userMake(self):
        self.first_name = input('Please enter your first name: \n')
        self.last_name = input('Please enter your last name: \n')
        print(f'Welcome {self.first_name} {self.last_name}!')
        
        self.username = input('Pick a username: \n')
        self.password = input('Pick a password: \n')
        cur = conn.cursor()
        sql_user = "INSERT INTO bank.users (first_name, last_name, username, pwd) VALUES (%s, %s, %s, %s) RETURNING id;"
        data_user = (self.first_name, self.last_name, self.username, self.password)
        cur.execute(sql_user, data_user)
        user_id = cur.fetchone()[0]

        sql_account = "INSERT INTO bank.accounts (user_id, account_type, balance) VALUES (%s, %s, %s);"
        data_account = (user_id, "Checking", 0)
        cur.execute(sql_account, data_account)

        conn.commit()
        cur.close()

class Account:
    # Class for getting account information
    pass

zach = createUser()
zach.userMake()