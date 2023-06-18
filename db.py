import sqlite3
import os
import traceback


from datetime import datetime
from log import log

class db:
    
    # Returns a connection to found db or to newly created 
    def connect(path):
        try:
            log.info(f'Connecting to database {path}')
            db.check_db_file(path)
            conn = sqlite3.connect(path)
            log.info('DB connection established')
            return conn
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')


    # Disconnect        
    def disconnect(conn):
        conn.close()
        log.info('DB disconnected')
        return
    
    
    # If no DB file found - create a new one
    def check_db_file(path):
        try:
            if not os.path.exists(path):
                log.warning('No DB file found! Creating a new one')
                conn = sqlite3.connect(path)
                conn.commit()
                conn.close
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')
            
                
    # convert yaml to db table
    def yaml_to_sql(conn, table, data):
        try:
            if db.check_table(conn, table) == False:
                log.info(f'Table {table} not found, creating.')
                db.create_table(conn, table)
            for id in data:
                h = hash(frozenset(data[id]))
                if db.check_hash(conn, table, id, h) == False:     
                    log.critical(f'TODO close old record')                                      
                    # db.close_old_record(conn, table, id, data[id], h)
                db.add_new_record(conn, table, id, data[id], h)                   
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}') 

    
    # check if table exists
    def check_table(conn, name):
        try: 
            cursor = conn.cursor()
            q = f"""
                SELECT name 
                FROM sqlite_master 
                WHERE type='table' 
                AND name='{name}'
                """
            cursor.execute(q)
            if cursor.fetchone() is None:
                return False        
            log.info(f'Table {name} found')
            return True
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}') 
            
    
    # create new table
    def create_table(conn, name):
        try:
            cursor = conn.cursor()
            q = f"""
                CREATE TABLE {name}
                (
                    uid INTEGER PRIMARY KEY,
                    {name}_id   INTEGER,
                    hash        INTEGER,
                    start_date  DATE,
                    end_date    DATE
                )"""
            cursor.execute(q)
            cursor.close()
            log.info(f'Table {name} created')
            return
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}') 
    
    
    # check if a row can be skipped by comparing hash
    def check_hash(conn, table, id, h):
        try:
            cursor = conn.cursor()
            q = f"""
                SELECT hash
                FROM {table}
                WHERE {table}_id = {id}
                """ 
            cursor.execute(q)
            row = cursor.fetchone()
            if row is not None:
                return True
            return False
                         
            
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}') 
    
    
    # closes old record
    def close_old_record(conn, table, id, data, h):
        log.info('TODO: close old record')
        
        
    # adds old record
    def add_new_record(conn, table, id, data, h):
        try:
            db.check_columns(conn, table, data)
            q_obj = db.get_insert_query(table, id, data, h) 
            q = q_obj['query']
            values = q_obj['values']
            cursor = conn.cursor()
            cursor.execute(q, values)
            conn.commit()
            log.info(f'Record {id}({h}) added')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}')    
    
    
    # check by row data if table column exists
    def check_columns(conn, table, row):
        try:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table})")
            rows = cursor.fetchall()
            column_names = [row[1] for row in rows]
            for att in row:
                if db.cnt_col_occur(att, column_names) > 0:
                    continue
                t = type(row[att])
                db.add_table_column(conn, table, att, t)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}') 
    
    
    # counts the occurence of column name in array of names   
    def cnt_col_occur(value, array):
        return sum([string.count(value) for string in array])
    
    
    # adds new table column of specified type
    def add_table_column(conn, table, att_name, att_type):
        try:
            col_type = db.get_column_type(att_type)
            if not att_type in (int, float, str):
                return 
            cursor = conn.cursor()
            alter_query = f"""
                ALTER TABLE {table} 
                ADD COLUMN {att_name} {col_type}
                """
            cursor.execute(alter_query)
            conn.commit()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            log.critical(f'ERROR in {method_name}: {e}') 
            
    
    # parse yaml type to sql        
    def get_column_type(att_type):
        if att_type == int:
            return 'INTEGER'
        elif att_type == float:
            return 'REAL'
        elif att_type == str:
            return 'TEXT'
        else: 
            return None
    
    
    def get_insert_query(table, id, data, h): 
        columns = []
        values = []
        
        # add id
        columns.append(table+"_id")
        values.append(id)
        
        # add hash
        columns.append("hash")
        values.append(h)
        
        # add dates
        columns.append("start_date")
        values.append(datetime.now())
        columns.append("end_date")
        values.append(datetime(9999, 12, 31, 23, 59, 59, 0))
        
        for att in data:
            if not type(data[att]) in (int, float, str):
                continue
            columns.append(att)
            values.append(data[att])
        
        query = f"""
            INSERT INTO {table} ({", ".join(columns)})
            VALUES ({", ".join(["?" for _ in values])})
        """                    
        return {'query': query, 'values': tuple(values)}
    
        # insert_query = "INSERT INTO your_table (column1, column2, column3) VALUES (?, ?, ?)"
        # values = ('value1', 'value2', 'value3')
       