import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class typeDogma(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.attributes = table_attributes()
        self.effects = table_effects()
        
    
    # check if all tables are present
    def check(self):
        try:
            # attributes
            self.check_table(self.attributes)
            
            # effects
            self.check_table(self.effects)
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
            self.db.table_start_sync(self.attributes.table_name)
            self.db.table_start_sync(self.effects.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_dogma(self.attributes, id, row, 'dogmaAttributes')
            self.add_dogma(self.effects, id, row, 'dogmaEffects')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.attributes.table_name)
            self.db.table_finish_sync(self.effects.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update services   
    def add_dogma(self, table_obj, id, row, node):
        try:
            t_name = table_obj.table_name
            t_pk = table_obj.table_pk
            data = self.yaml_value_extract(id, row, node)
            if len(data) == 0:
                return
            for item in data:
                columns = []
                values = []
                for column in table_obj.columns:
                    value = self.yaml_value_extract(id, item, column.path)
                    columns.append(column.name)
                    values.append(value)
                self.db.record_add_or_replace(t_name, t_pk, id, columns, values)
            # self.log.info(f'item {id} processed for {table_obj.table_name}')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
        
class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_attributes:
    def __init__(self):
        self.table_name = 'type_attributes'
        self.table_pk = 'type_id'
        self.columns = []
        
        self.columns.append(col('type_id',      'NUMBER', '#root'))
        self.columns.append(col('attribute_id', 'NUMBER', 'attributeID'))
        self.columns.append(col('value',        'NUMBER', 'value'))
        
        
class table_effects:
    def __init__(self):
        self.table_name = 'type_effects'
        self.table_pk = 'type_id'
        self.columns = []
        
        self.columns.append(col('type_id',      'NUMBER', '#root'))
        self.columns.append(col('effect_id',    'NUMBER', 'effectID'))
        self.columns.append(col('is_default',   'TEXT', 'isDefault'))
