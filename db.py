import sqlite3
import os
import traceback

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
                    # TODO - hash check and attribute check                    
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
    
    
    
    
    
    
    
    
    
    
    
    # # add data to table
    # def update_table(conn, table, yaml):
    #     columns = {}
    #     columns = db.get_yaml_columns(columns, yaml)
    #     db.check_table_columns(conn, table, columns)
    #     log.info('DUMMY')
    
    
    # # check if all columns exists
    # def check_table_columns(conn, table, yaml_cols):
    #     try:
    #         cursor = conn.cursor()
    #         cursor.execute(f"PRAGMA table_info({table})")
    #         table_cols = cursor.fetchall()
            
    #         for y_col in yaml_cols:
    #             for t_col in table_cols:
    #                 if y_col.name == t_col:
    #                     continue
    #                 db.add_table_column(conn, table, y_col.name, y_col.type)
    #     except Exception as e:
    #         method_name = traceback.extract_stack(None, 2)[0][2]
    #         log.critical(f'ERROR in {method_name}: {e}') 

            
    # # add a column if needed
    # def add_table_column(conn, table, column, type):    
    #     try:
    #         cursor = conn.cursor()
    #         alter_query = """ALTER TABLE {table} 
    #                         ADD COLUMN {column} {type}"""
    #         cursor.execute(alter_query)
    #         conn.commit()
    #     except Exception as e:
    #         method_name = traceback.extract_stack(None, 2)[0][2]
    #         log.critical(f'ERROR in {method_name}: {e}') 
        
    
    # # check if old record exists
    # def check_old_row(conn):
    #     log.info('DUMMY')
        
    
    # # add new record
    # def add_row(conn):
    #     log.info('DUMMY')


    # # get obj columns
    # def get_yaml_columns(columns, yaml, prefix=''):   
    #     # for record in yaml.items():
    #     #     b = record
    #     return columns