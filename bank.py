from dotenv import load_dotenv
import os

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

class User:
    # Class for creating/getting user
    pass

class Account:
    # Class for getting account information
    pass

