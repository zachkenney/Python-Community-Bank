from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

# Establish the connection to the DB. The variables here will pull from the .env file
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
# Function for testing connection to database
def connectionVerify():
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    print(cursor.fetchone())

# Class used for creating users.
class createUser:
    def __init__(self):
        pass

    def userMake(self): # Creates a user
        self.first_name = input('Please enter your first name: \n') # Saving as first name
        self.last_name = input('Please enter your last name: \n') # Saving as last name
        print(f'Welcome {self.first_name} {self.last_name}!')
        
        self.username = input('Pick a username: \n') # Pick username, save it as username
        self.password = input('Pick a password: \n') # Pick password, save it as password
        cur = conn.cursor() # Create a cursor using psycopg2
        sql_user = "INSERT INTO bank.users (first_name, last_name, username, pwd) VALUES (%s, %s, %s, %s) RETURNING id;" # Entering all the collected variables into the db
        data_user = (self.first_name, self.last_name, self.username, self.password) # Passing in the variables separately.
        # If I read the psycopg2 docs right, this is the safest way to do this.
        cur.execute(sql_user, data_user) # Executing
        user_id = cur.fetchone()[0] # Grabbing the id since I made it SERIAL primary key

        sql_account = "INSERT INTO bank.accounts (user_id, account_type, balance) VALUES (%s, %s, %s);" # Also setting up user on the accounts table
        data_account = (user_id, "Checking", 0) # passing in the previously retrieved Id to pass in as FK. For now just making this checking for $0
        cur.execute(sql_account, data_account)

        conn.commit()


def logIn():
    u = input('Please enter your username: \n') # Grabbing username
    p = input('Please enter your password: \n') # Grabbing password
    try:
        cur = conn.cursor()
        cur.execute('SELECT id from bank.users where username = %s;', (u, ))
        userId = cur.fetchone()[0] # Querying DB for given username and getting id for that row
        
        cur.execute('SELECT id from bank.users where pwd = %s;', (p, ))
        userpass = cur.fetchone()[0] # Querying DB for given password and getting id for that row

        if userpass == userId: # If username and password exist and are on same row they should have same id
            print('\nWelcome back!') 

        cur.close()
        conn.close()
    except:
        print('Username and password not found.')


class Account:
    # Class for getting account information
    pass

logIn()