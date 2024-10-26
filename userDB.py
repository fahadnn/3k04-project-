import sqlite3
import hashlib
import os

# Creating database file if not already exists
def create_db(dbName="users.db"):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    # Create table to store user information with user_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            salt TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    
#hash password with salt added
def _hash_password(password, salt):
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

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
    
    # Check if username already exists in the database
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        conn.close()
        return False, "Error, username already exists!"
    
    #creates salt and hashes password
    salt = os.urandom(16).hex()
    hashed_password = _hash_password(password, salt)
    
    #store user information
    cursor.execute("INSERT INTO users (username, salt, password) VALUES (?, ?, ?)", (username, salt, hashed_password))
    
    conn.commit()
    conn.close()
    return True, "Success, user registered!"

# Checks if login inputs match data in database, and return verification status
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, salt, password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    #Username not in database
    if result is None:
        return False, None
    
    #hashes password inputted by user and stored salt value
    user_id, stored_salt, stored_hashed_password = result
    hashed_password = hash_password(password, stored_salt)
    
    #successful login if hashed passwords match
    if hashed_password == stored_hashed_password:
        return True, user_id
    else:
        return False, None