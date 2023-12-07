import os
import sqlite3
import traceback

from log import log
lg = log(None)

class db_utils:
    
    def __init__(self, db_path, conn):
        self.db_path = db_path
        self.db_conn = conn
    
    
    # check if db exists, create if not
    def db_check(self):
        if not os.path.exists(self.db_path):
            self.db_create()
        
        
    # create static db file by path
    def db_create(self):
        conn = sqlite3.connect(self.db_path)
        conn.close()
        
    
    # establish connection
    def db_connect(self):
        try:
            self.db_check()
            self.db_conn = sqlite3.connect(self.db_path)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
    
    
    # close connection
    def db_disconnect(self):
        try:
            self.db_conn.close()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
        
        
    # check if table exists
    def table_check(self, table: str):
        try:
            _cursor = self.db_conn.cursor()
            q = f"""
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' 
                AND name='{table}'
                """
            _cursor.execute(q)
            if _cursor.fetchone() is None:
                return False
            return True
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
        
        
    # create table
    def table_create(self, table: str):
        blah = 123