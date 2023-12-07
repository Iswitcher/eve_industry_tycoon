import yaml

from db.db_utils import db_utils

import traceback
from log import log
lg = log(None)

class sde2db:
    
    def __init__(self, checksum):
        self.checksum = checksum
        self.sde_db_path = 'sde.db'
        
        self.sde_categories = 'sde/fsd/categoryIDs.yaml' 
    
    
    # main conversion method
    def sde_convert_all(self):
        self.sde_covert_categoryids()
        # TODO other types
        
    
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
        db = db_utils(self.sde_db_path, None)
        conn = db.db_connect()
        
        if not db.table_check(table):
            db.table_create(table)
        db.table_column_check(table, columns, types)
    
    
    # convert categoryIDs.yaml to DB
    def sde_covert_categoryids(self):    
        try:
            table = 'category_ids'
            columns = ['category_id', 'en']
            types = ['NUMBER', 'TEXT']
            
            self.sde_table_check(table, columns, types)
            
            yaml_data = self.sde_yaml_read(self.sde_categories)
            for row in yaml_data:
                b = row
                blah = 123
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
    