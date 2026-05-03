-----------------------------------------------------------------------------
PYTHON COMMUNITY BANK
-----------------------------------------------------------------------------

Simple bank emulation using Python and a self-hosted PostgreSQL database.
I created this to practice OOP and working with databases.
The program creates bank members, allows members to login, and deposit, withdraw and check their accounts.

To run this you'll need:
1. A postgreSQL db of your own.
2. In your DBMS, sequentially run the statements in the dbsetup.sql file provided. This creates the necessary schema and tables.
3. Install psycopg2-binary, python-dotenv.
4. Create a .env file (template included) which will hold the credentials for your DB.
5. Run the bank.py file.