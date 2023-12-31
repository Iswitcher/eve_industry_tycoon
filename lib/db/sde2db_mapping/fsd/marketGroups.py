import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class marketGroups(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.market_groups = table_market_groups()
        
    
    # check if all tables are present
    def check(self):
        try:
            # market_groups
            self.check_table(self.market_groups)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.market_groups.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_market_group(self.market_groups.table_name, self.market_groups.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.market_groups.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update market_groups   
    def add_market_group(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.market_groups.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        

class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_market_groups:
    def __init__(self):
        self.table_name = 'market_groups'
        self.table_pk = 'market_group_id'
        self.columns = []
        
        self.columns.append(col('market_group_id',  'NUMBER', '#root'))
        self.columns.append(col('name_en',          'TEXT', 'nameID/en'))
        self.columns.append(col('desc_en',          'TEXT', 'descriptionID/en'))
        self.columns.append(col('has_types',        'TEXT', 'hasTypes'))
        self.columns.append(col('icon_id',          'NUMBER', 'iconID'))
        self.columns.append(col('parent_group_id',  'NUMBER', 'parentGroupID'))
        