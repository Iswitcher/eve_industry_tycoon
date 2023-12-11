import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class ancestries(mapper):
    
    def __init__(self, db_path, yaml, log):
        self.db_path = db_path
        self.yaml = yaml
        self.log = log
        self.db = db_utils(self.log, self.db_path, None)
        
        self.table_ancestries = 'ancestries'
        self.table_ancestries_pk = 'ancestry_id'


    def run(self):
        try:
            self.db.db_check()
            self.db.db_connect()
            
            self.check_tables_and_columns()
            self.sync()
            
            self.db.db_commit()
            self.db.db_disconnect()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    #go row by row and fill each table
    def sync(self):
        try:
            self.db.table_start_sync(self.table_ancestries)
            for row in self.yaml:
                # add row to agents table
                self.add_agent(self.table_ancestries, self.table_ancestries_pk, row, self.yaml[row])
            self.db.table_finish_sync(self.table_ancestries)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    # check all class-cpecific tables and columns
    def check_tables_and_columns(self):
        try:
            # agents
            if not self.db.table_check(self.table_ancestries):
                self.db.table_create(self.table_ancestries)
            agent_columns, agent_types = self.get_agent_columns()
            self.db.table_column_check(self.table_ancestries, agent_columns, agent_types)  
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    # get yaml value by path or fill None if not found
    def yaml_value_extract(self, yaml_row, path):
        path_array = path.split('/')
        result = yaml_row
        try:
            for node in path_array:
                result = result.get(node)
            return result
        except (KeyError, TypeError):
            return None
    

    # get the list of columns in table: agents
    def get_agent_columns(self, columns = [], types = []):
        columns.append('ancestry_id')
        types.append('NUMBER')
        
        columns.append('bloodline_id')
        types.append('NUMBER')
        
        columns.append('icon_id')
        types.append('NUMBER')
        
        columns.append('name')
        types.append('TEXT')
        
        columns.append('short_desc')
        types.append('TEXT')
        
        columns.append('desc')
        types.append('TEXT')
        
        columns.append('charisma')
        types.append('NUMBER')
        
        columns.append('intelligence')
        types.append('NUMBER')
        
        columns.append('memory')
        types.append('NUMBER')
        
        columns.append('perception')
        types.append('NUMBER')
        
        columns.append('willpower')
        types.append('NUMBER')
        
        return columns, types    
         
    
    # add or update an agent        
    def add_agent(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            columns.append('ancestry_id')
            values.append(id)
            
            columns.append('bloodline_id')
            values.append(self.yaml_value_extract(row, 'bloodlineID'))
            
            columns.append('icon_id')
            values.append(self.yaml_value_extract(row, 'iconID'))
            
            columns.append('name')
            values.append(self.yaml_value_extract(row, 'nameID/en'))
            
            columns.append('short_desc')
            values.append(self.yaml_value_extract(row, 'shortDescription'))
            
            columns.append('desc')
            values.append(self.yaml_value_extract(row, 'descriptionID/en'))
            
            columns.append('charisma')
            values.append(self.yaml_value_extract(row, 'charisma'))
            
            columns.append('intelligence')
            values.append(self.yaml_value_extract(row, 'intelligence'))
            
            columns.append('memory')
            values.append(self.yaml_value_extract(row, 'memory'))
            
            columns.append('perception')
            values.append(self.yaml_value_extract(row, 'perception'))
            
            columns.append('willpower')
            values.append(self.yaml_value_extract(row, 'willpower'))
            
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    

