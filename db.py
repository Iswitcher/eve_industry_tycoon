import sqlite3
import os

from log import log

class db:
    
    # Returns a connection to found db or to newly created 
    def connect(path):
        try:
            db.check_db_file(path)
            conn = sqlite3.connect(path)
            log.info('DB connection established')
            return conn
        except Exception as e:
            log.critical('Failed to establish connection: {e}')   
            
    
    # Disconnect        
    def disconnect(conn):
        conn.close()        
    
    
    # If no DB file found - create a new one
    def check_db_file(path):
        if not os.path.exists(path):
            log.warning('No DB file found! Creating a new one')
            conn = sqlite3.connect(path)
            conn.commit()
            conn.close

    
    # Extract yaml into sql table
    def yaml_2_sql(conn, table, data):
        db.check_table(conn, table)
    
    
    # check if table exists
    def check_table(conn, name):
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT name 
                       FROM sqlite_master 
                       WHERE type='table' 
                       AND name=?
                       """, (name,))
        if cursor.fetchone() is None:
            log.warning(f'No table {name} is found, creating new.')
            db.create_table(conn, name)        
        return
            
    
    # create new table
    def create_table(conn, name):
        cursor = conn.cursor()
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS {name} 
                       (
                        uid INTEGER PRIMARY KEY,
                        start_date DATE,
                        end_date DATE
                        )""")
        log.info(f'Table {name} created')
        return

