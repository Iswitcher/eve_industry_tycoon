import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class controlTowerResources(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.resources = table_resources()
        
    
    # check if all tables are present
    def check(self):
        try:
            # controlTowerResources
            self.check_table(self.resources)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
    
    # check provided table obj
    def check_table(self, table_obj):
        try:
            if not self.db.table_check(table_obj.table_name):
                    self.db.table_create(table_obj.table_name)
            cols = [] 
            types = []
            for column in table_obj.columns:
                    cols.append(column.name)
                    types.append(column.type)
            self.db.table_column_check(table_obj.table_name, cols, types)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.resources.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_resources(self.resources.table_name, self.resources.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.resources.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update resources       
    def add_resources(self, table, pk, id, row):
        try:
            for resource in row['resources']:            
                columns = []
                values = []
                for column in self.resources.columns:
                    value = self.yaml_value_extract(id, resource, column.path)
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
    

class table_resources:
    def __init__(self):
        self.table_name = 'control_tower_resources'
        self.table_pk = 'control_tower_id'
        self.columns = []
        
        self.columns.append(col('control_tower_id', 'NUMBER', '#root'))
        self.columns.append(col('faction_id',       'NUMBER', 'factionID'))
        self.columns.append(col('purpose',          'NUMBER', 'purpose'))
        self.columns.append(col('quantity',         'NUMBER', 'quantity'))
        self.columns.append(col('resource_type_id', 'NUMBER', 'resourceTypeID'))