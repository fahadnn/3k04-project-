import sqlite3

# Creating database file if not already exists
def create_db(dbName="users.db"):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    # Create table to store user information with user_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    
# Registration validation and adds inputs to database
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Check the number of users in the database and return error if there are 10 already
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count >= 10:
        conn.close()
        return False, "Maximum number of users reached. Cannot register more than 10 users!"
    
    # Check if username already exists in the database; otherwise, add user info
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        conn.close()
        return False, "Error, username already exists!"
    
    # Initialize default programmable parameters field as empty JSON
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)) 
    
    conn.commit()
    conn.close()
    return True, "Success, user registered!"

# Checks if login inputs match data in database, and return verification status
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))  # Change 'id' to 'user_id'
    user = cursor.fetchone()
    conn.close()
    
    if user and user[1] == password:  # Check password
        return True, user[0]  # Return True and user ID if password matches username
    return False, None  #return false none if password is wrong 