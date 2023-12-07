import os
import sqlite3
import hashlib
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
                    hash        TEXT PRIMARY KEY,
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
            
            
    # close old record and add new one
    # does nothing if the record is unchanged
    def record_add_or_replace(self, table, id_name, id, columns, values):
        try:
            hash = self.get_record_hash_md5(values)
            old_hash = self.get_old_record_hash(table, id_name, id)
            if hash == old_hash:
                return
            if old_hash != None:
                self.record_close(table, id_name, id)
            blah = 123
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
        
    
    # pile all attributes and make a hash of it
    def get_record_hash_md5(self, values):
        try:
            md5 = hashlib.md5()
            md5.update(str(values).encode('utf-8'))
            return md5.hexdigest()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
    
    
    # get old record by id
    def get_old_record_hash(self, table, key, value):
        try:
            _cursor = self.db_conn.cursor()
            q = f"""
                SELECT hash
                FROM {table}
                WHERE {key} = {value}
                AND end_date > DATE('now')
                """
            _cursor.execute(q)
            row = _cursor.fetchone()
            if row is not None:
                return row[0]
            return None
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
        
        
    # set end date for old record
    def record_close(self, table, key, value):
        try:
            _cursor = self.db_conn.cursor()
            q = f"""
                UPDATE {table}
                SET end_date = DATE('now')
                WHERE {key} = {value}
                AND end_date > DATE('now')
                """
            _cursor.execute(q)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
    