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
    #setup database connection
    conn = sqlite3.connect('parameters.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT parameter, value FROM parameters WHERE user_id = ?', (user_id,))
    parameters = cursor.fetchall()
    
    conn.close()
    #return parameters
    # Convert the list of tuples into a dictionary
    return {param: value for param, value in parameters}