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
        print(f'\nWelcome {self.first_name} {self.last_name}!\n')
        
        self.username = input('Pick a username: \n') # Pick username, save it as username
        self.password = input('Pick a password: \n') # Pick password, save it as password
        cur = conn.cursor() # Create a cursor using psycopg2
        sql_user = 'INSERT INTO bank.users (first_name, last_name, username, pwd) VALUES (%s, %s, %s, %s) RETURNING id;' # Entering all the collected variables into the db
        data_user = (self.first_name, self.last_name, self.username, self.password) # Passing in the variables separately.
        # If I read the psycopg2 docs right, this is the safest way to do this.
        cur.execute(sql_user, data_user) # Executing
        user_id = cur.fetchone()[0] # Grabbing the id since I made it SERIAL primary key

        sql_account = 'INSERT INTO bank.accounts (user_id, account_type, balance) VALUES (%s, %s, %s);' # Also setting up user on the accounts table
        data_account = (user_id, "Checking", 0) # passing in the previously retrieved Id to pass in as FK. For now just making this checking for $0
        cur.execute(sql_account, data_account)

        conn.commit()

def logIn():
    while True:
        u = input('\nPlease enter your username: \n') # Grabbing username
        p = input('Please enter your password: \n') # Grabbing password    
        try:
            cur = conn.cursor()
            command = 'SELECT id, username, first_name, last_name FROM bank.users WHERE username = %s and pwd = %s;'
            data =  (u, p)
            cur.execute(command, data)
            result = cur.fetchone() # Querying DB for given username and getting id for that row
            cur.close()

            if result:
                print('Login Successful!')
                return User(result[0], result[1], result[2], result[3])

            else:
                print('Username or password incorrect. Please try again.')
        except Exception as e:
            print(e)

class User:
    def __init__(self, user_id, username, first_name, last_name):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

class Account:
    def __init__(self, user_id):
        self.user_id = user_id

    def getAccounts(self):
        cur = conn.cursor()
        account_query = 'SELECT id, account_type, balance FROM bank.accounts WHERE user_id = %s;'
        data = (self.user_id, )
        cur.execute(account_query, data)
        accounts = cur.fetchone()
        return accounts

    def getBalance(self, accounts):
        account_type = accounts[1]
        account_amount = accounts[2]

        print(f'Your {account_type} account balance is {account_amount}.')

    def updateBalance(self, accounts, amount):
        cur = conn.cursor()
        account_id = accounts[0]
        balance = 'SELECT sum(amount) FROM bank.transactions WHERE account_id = %s;'
        cur.execute(balance, (account_id, ))
        current_balance = cur.fetchone()[0]


        if int(current_balance) + int(amount) < 0:
            print('Insuffienct funds!')
        else:
            insert = 'INSERT INTO bank.transactions (account_id, amount) VALUES (%s, %s);'
            values = (account_id, amount)
            cur.execute(insert, values)
            
            new_balance = int(current_balance) + int(amount)
            update = 'UPDATE bank.accounts SET balance = %s WHERE id = %s;'
            data = (new_balance, account_id)
            cur.execute(update, data)
            conn.commit()
        
        conn.commit()
        cur.close()

    def deposit(self, accounts):
        amount = int(input('How much are you depositing? \n > '))
        self.updateBalance(accounts, amount)
        

    def withdraw(self, accounts):
        amount = int('-' + input('How much are you withdrawing? \n > '))
        self.updateBalance(accounts, amount)

def accountMenu(current_user):
    useraccount = Account(current_user.user_id)
    accounts = useraccount.getAccounts()

    while True:
        function_select = input('\nWhat would you like to do today? \n \
        1. Check balance \n \
        2. Deposit funds \n \
        3. Withdraw funds \n \
        4. Exit \n \
        > ')
    
        if function_select == '1':
            useraccount.getBalance(accounts)
        elif function_select == '2':
            useraccount.deposit(accounts)
            accounts = useraccount.getAccounts()
        elif function_select == '3':
            useraccount.withdraw(accounts)
            accounts = useraccount.getAccounts()
        elif function_select == '4':
            break
        else:
            print('Invalid selection.')

def cli():
    print('\nWELCOME TO PYTHON COMMUNITY BANK\n')
    
    while True:
        user_start = input('Are you a new member or an existing member?\n \
        1. New member\n \
        2. Existing member\n \
        > ')

        if user_start == '1':
            newUser = createUser()
            newUser.userMake()
            current_user = logIn()
            accountMenu(current_user)

            break
        elif user_start == '2':
            current_user = logIn()
            accountMenu(current_user)
            break
        else:
            print('Invalid selection.')

cli()

# Things To Do
# 1. Input validation on the deposit/withdraw amounts
# 2. Login failure handling X
