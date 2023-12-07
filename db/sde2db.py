import yaml

from db.db_utils import db_utils

import traceback
from log import log
lg = log(None)

class sde2db:
    
    def __init__(self, checksum):
        self.checksum = checksum
        # self.sde_db_path = 'sde.db'
        self.db = db_utils('sde.db', None)
        
        self.sde_categories = 'sde/fsd/categoryIDs.yaml' 
    
    
    # main conversion method
    def sde_convert_all(self):
        self.db.db_connect()
        
        self.sde_covert_categoryids()
        # TODO other types
        
        self.db.db_disconnect()
        
    
    # read yaml file
    def sde_yaml_read(self, path):
        try:
            with open(path, 'r', encoding="utf-8") as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
                return yaml_data
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
            
            
    # check if tables exists and check columns
    def sde_table_check(self, table, columns, types):
        if not self.db.table_check(table):
            self.db.table_create(table)
        self.db.table_column_check(table, columns, types)
        
        
    # insert into db a new record
    def sde_table_try_insert(self, table, id_name, id, columns, values):
        try:
            self.db.record_add_or_replace(table, id_name, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
    
    
    # convert categoryIDs.yaml to DB
    def sde_covert_categoryids(self):    
        try:
            table = 'category_ids'
            id_name = 'category_id'
            columns = ['category_id', 'en']
            types = ['NUMBER', 'TEXT']
            
            self.sde_table_check(table, columns, types)
            
            yaml_data = self.sde_yaml_read(self.sde_categories)
            for row in yaml_data:
                values = []
                values.append(row)
                values.append(yaml_data[row]['name']['en'])
                self.sde_table_try_insert(table, id_name, row, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            lg.critical(f'ERROR in {method_name}: {e}')
            
    