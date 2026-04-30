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
        self.first_name = input('Please enter your first name: \n')
        self.last_name = input('Please enter your last name: \n')


    def getName(self):
        print(f'Welcome {self.first_name} {self.last_name}!')
        cur = conn.cursor()
        cur.execute("INSERT INTO bank.users (first_name, last_name) VALUES (%s, %s)", (self.first_name, self.last_name))
        conn.commit()


class Account:
    # Class for getting account information
    pass

zach = createUser()
zach.getName()