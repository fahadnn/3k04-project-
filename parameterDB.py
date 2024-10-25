import sqlite3

def create_parameters_db():
    """Create the parameters database and the necessary table."""
    conn = sqlite3.connect('parameters.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parameters (
            user_id INTEGER NOT NULL,
            parameter TEXT NOT NULL,
            value REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    conn.commit()
    conn.close()

'''
def save_parameter(user_id, parameter, value):
    """Save a single parameter value for a user with retry mechanism."""
    if user_id is None:
        print("Error: user_id is None.")
        return  # Handle this case appropriately

    max_retries = 5
    for attempt in range(max_retries):
        try:
            conn = sqlite3.connect('parameters.db', timeout=5)  # Set a timeout
            cursor = conn.cursor()
            
            # Clear previous entries for this user before inserting new values
            cursor.execute('DELETE FROM parameters WHERE user_id = ?', (user_id,))
            cursor.execute('INSERT INTO parameters (user_id, parameter, value) VALUES (?, ?, ?)', (user_id, parameter, value))
            conn.commit()
            break  # Exit loop if successful
        except sqlite3.OperationalError as e:
            print(f"Attempt {attempt + 1}: {e}")
            time.sleep(0.1)  # Wait a moment before retrying
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")
            break  # Exit loop if there is an integrity error
        finally:
            conn.close()  # Ensure connection is closed even if an error occurs
'''            
# save all the parameters in the DB
def save_parameters(user_id, parameter_values):
    """Save multiple parameter values for a user."""
    conn = sqlite3.connect('parameters.db')
    cursor = conn.cursor()
    
    # Clear previous entries for this user
    cursor.execute('DELETE FROM parameters WHERE user_id = ?', (user_id,))
    
    # Insert new parameter values
    for parameter, value in parameter_values.items():
        cursor.execute('INSERT INTO parameters (user_id, parameter, value) VALUES (?, ?, ?)', 
                       (user_id, parameter, value))
    
    conn.commit()
    conn.close()

#get the parameter data for a specific user using the user id
def get_parameters(user_id):
    """Retrieve parameters for a specific user."""
    conn = sqlite3.connect('parameters.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT parameter, value FROM parameters WHERE user_id = ?', (user_id,))
    parameters = cursor.fetchall()
    
    conn.close()
    return parameters