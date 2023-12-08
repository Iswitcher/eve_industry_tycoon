import yaml

from cfg import cfg
from db.db_utils import db_utils

import traceback
from log import log

class sde2db:
    
    def __init__(self, checksum):
        # self.checksum = checksum
        self.lg = log(None)
        self.db = db_utils('sde.db', None)
        self.cfg = cfg()
    
    
    # main conversion method
    def sde_convert_all(self):
        self.db.db_connect()
        
        self.sde_covert_category_ids()
        self.sde_covert_market_groups()
        # self.sde_covert_inv_flags() # NON FUNCTIONAL
        # TODO other types
        
        self.db.db_disconnect()
        
    
    # read yaml file
    def sde_yaml_read(self, config):
        try:
            path = config.yaml_path
            with open(path, 'r', encoding="utf-8") as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
                return yaml_data
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.lg.critical(f'ERROR in {method_name}: {e}')
            
            
    # check if tables exists and check columns
    def sde_table_check(self, config):
        try:
            table = config.db_table
            columns = []
            types = []
            if not self.db.table_check(table):
                self.db.table_create(table)       
            for col in config.columns:
                columns.append(col.col)
                types.append(col.type)         
            self.db.table_column_check(table, columns, types)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.lg.critical(f'ERROR in {method_name}: {e}')
    
        
    # insert into db a new record
    def sde_table_try_insert(self, table, id_name, id, columns, values):
        try:
            self.db.record_add_or_replace(table, id_name, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.lg.critical(f'ERROR in {method_name}: {e}')
    
    
    # get the values from yaml and push to sql
    def sde_extract_and_convert(self, config):
        try: 
            self.sde_table_check(config)
            yaml_data = self.sde_yaml_read(config)
            for obj_id in yaml_data:
                row = yaml_data[obj_id]
                columns = []
                values = []
                for col in config.columns:
                    columns.append(col.col)
                    value = self.yaml_value_extract(obj_id, row, col.path)
                    values.append(value)
                self.sde_table_try_insert(config.db_table,config.pk_name, 
                    obj_id,columns,values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.lg.critical(f'ERROR in {method_name}: {e}')
    
    
    # get yaml value by path or fill None if not found
    def yaml_value_extract(self, id, yaml_row, path):
        path_array = path.split('/')
        result = yaml_row
        try:
            for node in path_array:
                if node == 'root' and len(path_array) == 1: 
                    return id
                if node == 'root' and len(path_array) > 1: 
                    continue
                result = result.get(node)
            return result
        except Exception as e:
            return None
    

    # convert categoryIDs.yaml
    def sde_covert_category_ids(self):
        cfg_path = 'config/sde2db_mapping/fsd/categoryIDs.json'
        config = self.cfg.get_config_json(cfg_path)
        self.sde_extract_and_convert(config)
    
    
    # convert marketGroups.yaml
    def sde_covert_market_groups(self):
        cfg_path = 'config/sde2db_mapping/fsd/marketGroups.json'
        config = self.cfg.get_config_json(cfg_path)
        self.sde_extract_and_convert(config)
        
        
    # convert invFlags.yaml
    # def sde_covert_inv_flags(self):
    #     cfg_path = 'config/sde2db_mapping/bsd/invFlags.json'
    #     config = self.cfg.get_config_json(cfg_path)
    #     self.sde_extract_and_convert(config)



