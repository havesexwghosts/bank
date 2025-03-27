import sqlite3
import os

def view_database_contents(db_path):
    try:
        # Check if the database file exists
        if not os.path.exists(db_path):
            print("Database file does not exist.")
            return
        
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute a query to fetch all data from the users table
        cursor.execute("SELECT * FROM users")
        
        # Fetch all results
        rows = cursor.fetchall()

        # Print the results
        if rows:
            print("Database records:")
            for row in rows:
                print(row)
        else:
            print("No records found in the users table.")
    
    except sqlite3.OperationalError as e:
        print(f"Operational error: {e}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

# Provide the path to your database
db_path = "file_path"
view_database_contents(db_path)