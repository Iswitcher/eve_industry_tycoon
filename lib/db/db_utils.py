import os
import sqlite3
import hashlib
import traceback
from datetime import datetime

class db_utils:
    
    def __init__(self, db_path, conn, log):
        self.db_path = db_path
        self.db_conn = conn
        self.log = log
    
    
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
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # close connection
    def db_disconnect(self):
        try:
            self.db_conn.close()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        
        
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
            self.log.critical(f'ERROR in {method_name}: {e}')
        
        
    # create table
    def table_create(self, table: str):
        try:
            _cursor = self.db_conn.cursor()
            q = (f"""
                CREATE TABLE {table}
                (
                    hash        TEXT,
                    is_updated  NUMBER,
                    start_date  DATE,
                    end_date    DATE
                )""")
            _cursor.execute(q)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        
    
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
                self.table_column_add(table, att, type)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
    
    # counts the occurence of column name in array of names
    def cnt_col_occur(self, value, array):
        cnt = 0
        for i in array:
            if i == value:
                cnt = cnt + 1
        return cnt
    
    
    # adds new table column of specified type
    def table_column_add(self, table, att_name, att_type):
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
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    # close old record and add new one
    # does nothing if the record is unchanged
    def record_add_or_replace(self, table, id_name, id, columns, values):
        try:
            hash = self.get_record_hash_md5(values)
            old_hash = self.get_old_record_hash(table, id_name, id)
            if hash == old_hash:
                self.record_set_is_updated(table, id_name, id)
                return
            if old_hash != None:
                self.record_close(table, id_name, id)
            self.record_add(table, hash, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        
    
    # pile all attributes and make a hash of it
    def get_record_hash_md5(self, values):
        try:
            md5 = hashlib.md5()
            md5.update(str(values).encode('utf-8'))
            return md5.hexdigest()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.logger.critical(f'ERROR in {method_name}: {e}')
    
    
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
            self.log.critical(f'ERROR in {method_name}: {e}')
        
        
    # set end date for old record
    def record_close(self, table, key, value):
        try:
            _cursor = self.db_conn.cursor()
            q = f"""
                UPDATE {table}
                SET end_date = DATETIME('now'),
                    is_updated = 1
                WHERE {key} = {value}
                AND end_date > DATETIME('now')
                """
            _cursor.execute(q)
            self.db_conn.commit()
            _cursor.close()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    def record_set_is_updated(self, table, key, value):
        try:
            _cursor = self.db_conn.cursor()
            q = f"""
                UPDATE {table}
                SET is_updated = 1
                WHERE {key} = {value}
                AND end_date > DATETIME('now')
                """
            _cursor.execute(q)
            self.db_conn.commit()
            _cursor.close()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    # add new record
    def record_add(self, table, hash, columns, values):
        try:
            # add hash
            columns.append("hash")
            values.append(hash)
            
            # add is_updated_flag
            columns.append("is_updated")
            values.append(1)
            
            # add dates
            columns.append("start_date")
            values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            columns.append("end_date")
            values.append(datetime(9999, 12, 31, 23, 59, 59, 0))
            
            q_obj = self.get_insert_query(table, columns, values)
            _cursor = self.db_conn.cursor()
            _cursor.execute(q_obj['query'], q_obj['values'])
            self.db_conn.commit()
            _cursor.close()  
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        
    
    def get_insert_query(self, table, columns, values):
        # str_values = [str(value) for value in values]
        query = f"""
            INSERT INTO {table} ({", ".join(columns)})
            VALUES ({", ".join(["?" for _ in values])})
        """
        return {'query': query, 'values': tuple(values)}
    

    # unflag all rows before sync
    def table_start_sync(self, table):
        try:
            _cursor = self.db_conn.cursor()
            q = f"""
                UPDATE {table}
                SET is_updated = 0
                WHERE end_date > DATETIME('now')
                """
            _cursor.execute(q)
            self.db_conn.commit()
            _cursor.close()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # close all rows which weren't in yaml
    def table_finish_sync(self, table):
        try:
            _cursor = self.db_conn.cursor()
            q = f"""
                UPDATE {table}
                SET is_updated = 1, 
                    end_date = DATETIME('now')
                WHERE is_updated = 0
                AND end_date > DATETIME('now')
                """
            _cursor.execute(q)
            self.db_conn.commit()
            _cursor.close()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')