import sqlite3, os

class Database:
    def __init__(self, db_directory="./data", db_name="bank.db"):
        # Initialize database directory and file name
        self.db_directory = os.path.abspath(db_directory)  # Get absolute path of the directory
        self.db_name = db_name  # Database file name
        self.db_path = os.path.join(self.db_directory, self.db_name)  # Full path of the database file
        
        # Check if the database file exists; if not, create the directory
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_directory)  # Create directory if it doesn't exist

    # Method to establish a connection to the SQLite database
    def get_db_connection(self):
        conn = sqlite3.connect(self.db_path)  # Connect to the SQLite database
        conn.row_factory = sqlite3.Row  # Enable access to columns by name (instead of index)
        return conn  # Return the connection object
    
    # Method to check if a user already exists in the database
    def user_exists(self, name):
        conn = self.get_db_connection()  # Get the database connection
        cursor = conn.cursor()  # Create a cursor object to interact with the database
        
        print(f"Executing query: SELECT 1 FROM users WHERE name = {name}")  # Debug print for the executed query
        
        cursor.execute("SELECT 1 FROM users WHERE name = ?", (name,))  # Execute query to check if user exists
        result = cursor.fetchone()  # Fetch the result (either None or a match)
        
        print(f"Query result: {result}")  # Debug print to show the query result

        conn.close()  # Close the database connection
        return result is not None  # Return True if user exists, otherwise False
    
    # Method to fetch user details by username
    def get_user_by_name(self, name):
        conn = self.get_db_connection()  # Get the database connection
        user = conn.execute('SELECT * FROM users WHERE name = ?', (name,)).fetchone()  # Fetch the user by name
        conn.close()  # Close the connection
        return user  # Return the user data (or None if not found)
    
    # Method to update the user's balance
    def update_balance(self, name, new_balance):
        conn = self.get_db_connection()  # Get the database connection
        conn.execute('UPDATE users SET balance = ? WHERE name = ?', (new_balance, name))  # Execute balance update query
        conn.commit()  # Commit the transaction to the database
        conn.close()  # Close the connection

    # Method to create a new user in the database
    def create_user(self, name, password, balance):
        conn = self.get_db_connection()  # Get the database connection
        conn.execute('INSERT INTO users (name, password, balance) VALUES (?, ?, ?)', (name, password, balance))  # Insert new user
        conn.commit()  # Commit the transaction
        conn.close()  # Close the connection

    # Method to insert a sample user into the database (for testing purposes)
    def insert_sample_user(self):
        try:
            conn = self.get_db_connection()  # Get the database connection
            cursor = conn.cursor()  # Create a cursor object
            
            # Insert a sample user into the users table
            cursor.execute('INSERT INTO users (name, password, balance) VALUES (?, ?, ?)', ('test_user', 'password123', 100))
            conn.commit()  # Commit the transaction
            print("Sample user inserted.")  # Debug print message
        except Exception as e:
            print(f"Error inserting user: {e}")  # Error handling if something goes wrong
        finally:
            conn.close()  # Ensure the connection is closed

    # Method to initialize the database (create tables if they don't exist)
    def init_db(self):
        try:
            conn = self.get_db_connection()  # Get the database connection
            cursor = conn.cursor()  # Create a cursor object
            
            # SQL query to create the 'users' table if it doesn't already exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  # Auto-incrementing primary key
                    name TEXT NOT NULL,  # Name column (unique)
                    password TEXT NOT NULL,  # Password column
                    balance INTEGER NOT NULL  # Balance column
                )
            ''')

            conn.commit()  # Commit the transaction
            print("Database initialized successfully. Table created if not exists.")  # Debug print message
        except Exception as e:
            print(f"Error initializing database: {e}")  # Error handling if something goes wrong
        finally:
            conn.close()  # Ensure the connection is closed