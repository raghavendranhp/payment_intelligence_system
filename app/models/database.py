import sqlite3
import os

def get_db_path() -> str:
    """
    Dynamically resolves the absolute path to the SQLite database file.
    This ensures the application always finds the database regardless of 
    where the uvicorn server is launched from.
    """
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_dir, "data", "payments.db")

def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    This will be used by the Pandas analyzer to fetch specific rows.
    """
    db_path = get_db_path()
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Database not found at {db_path}. "
            "Please run 'python init_db.py' first to generate the database from the CSV."
        )
        
    # Establish the connection
    conn = sqlite3.connect(db_path)
    
    
    conn.row_factory = sqlite3.Row 
    
    return conn