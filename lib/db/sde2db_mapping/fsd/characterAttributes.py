import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class characterAttributes(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.attributes = table_attributes()
        
    
    # check if all tables are present
    def check(self):
        try:
            # characterAttributes
            self.check_table(self.attributes)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.attributes.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_attribute(self.attributes.table_name, self.attributes.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.attributes.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update a attribute        
    def add_attribute(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.attributes.columns:
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
    

class table_attributes:
    def __init__(self):
        self.table_name = 'character_attributes'
        self.table_pk = 'attribute_id'
        self.columns = []
        
        self.columns.append(col('attribute_id', 'NUMBER', '#root'))
        self.columns.append(col('name_en',      'TEXT', 'nameID/en'))
        self.columns.append(col('description',  'TEXT', 'description'))
        self.columns.append(col('notes',        'TEXT', 'notes'))
        self.columns.append(col('short_desc',   'TEXT', 'shortDescription'))