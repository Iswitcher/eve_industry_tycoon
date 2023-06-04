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
        conn.close        
    
    
    # If no DB file found - create a new one
    def check_db_file(path):
        if not os.path.exists(path):
            log.warning('No DB file found! Creating a new one')
            conn = sqlite3.connect(path)
            conn.commit()
            conn.close

    
     # create sql table if not exsists  
    # def check_table(db_path, table):
    #     try:
    #         conn = sqlite3.connect(db_path)
    #         if self.table_exists(table, conn):
    #             self.log(f'The table {table} exists.')
    #         else:
    #             self.log(f'The table {table} does not exist. Creating.')
    #             self.sql_create_new_table(conn, table)
    #         conn.close
    #     except Exception as e:
    #         log.critical('Error while checking db table: {e}') 
    
        # check if sql table exists
    # def table_exists(self, table, conn):
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    #     return cursor.fetchone() is not None
    
        # create table with standard fields 
    # def sql_create_new_table(self, conn, table):
    #     cursor = conn.cursor()
    #     cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table} (
    #                 uid INTEGER PRIMARY KEY,
    #                 start_date DATE,
    #                 end_date DATE
    #             )''')
    #     self.log(f'Table {table} created!')  

    # # extract yaml into sql table
    # def extract_yaml(self, file):
    #     try:
    #         table = self.yaml_get_table_name(file)
    #         self.check_or_create_sql_table(table)
    #     except Exception as e:
    #         self.log(f'Error while extracting yaml: {e}', 'e')   

