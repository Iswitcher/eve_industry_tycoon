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
        try:
            _cursor = self.db_conn.cursor()
            q = (f"""
                CREATE TABLE {table}
                (
                    checksum    TEXT,
                    start_date  DATE,
                    end_date    DATE
                )""")
            _cursor.execute(q)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
        
    
    # check if table columns exist
    def table_column_check(self, table: str, columns, types):
        try:
            if len(columns) != len(types):
                raise Exception("Mismatch lenght of columns/types!")
            _cursor = self.db_conn.cursor()
            _cursor.execute(f"PRAGMA table_info({table})")
            rows = _cursor.fetchall()
            column_names = [row[1] for row in rows]
            for i, att in enumerate(columns):
                if self.cnt_col_occur(att, column_names) > 0:
                    continue
                type = types[i]
                self.add_table_column(table, att, type)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
            
    
    # counts the occurence of column name in array of names
    def cnt_col_occur(self, value, array):
        cnt = 0
        for i in array:
            if i == value:
                cnt = cnt + 1
        return cnt
    
    
    # adds new table column of specified type
    def add_table_column(self, table, att_name, att_type):
        try:
            _cursor = self.db_conn.cursor()
            alter_query = f"""
                ALTER TABLE {table} 
                ADD COLUMN {att_name} {att_type}
                """
            _cursor.execute(alter_query)
            self.db_conn.commit()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')