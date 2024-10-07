import sqlite3

def createDB(dbName = "users.db"):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL  
        )""")
    
    conn.commit()
    conn.close()