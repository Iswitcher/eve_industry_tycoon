import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class ancestries(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.ancestries = table_ancestries()


    # check if all tables are present
    def check(self):
        try:
            # ancestries
            if not self.db.table_check(self.ancestries.table_name):
                self.db.table_create(self.ancestries.table_name)
            ancestry_cols = [] 
            ancestry_types = []
            for column in self.ancestries.columns:
                ancestry_cols.append(column.name)
                ancestry_types.append(column.type)
            self.db.table_column_check(self.ancestries.table_name, ancestry_cols, ancestry_types)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.ancestries.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_ancestry(self.ancestries.table_name, self.ancestries.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.ancestries.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}') 

    
    # add or update an ancestry        
    def add_ancestry(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.ancestries.columns:
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
    

class table_ancestries:
    def __init__(self):
        self.table_name = 'ancestries'
        self.table_pk = 'ancestry_id'
        self.columns = []
        
        self.columns.append(col('ancestry_id',  'NUMBER', '#root'))
        self.columns.append(col('bloodline_id', 'NUMBER', 'bloodlineID'))
        self.columns.append(col('icon_id',      'NUMBER', 'iconID'))
        self.columns.append(col('name_en',      'TEXT', 'nameID/en'))
        self.columns.append(col('short_desc_en','TEXT', 'shortDescription'))
        self.columns.append(col('desc_en',      'TEXT', 'descriptionID/en'))
        self.columns.append(col('charisma',     'NUMBER', 'charisma'))
        self.columns.append(col('intelligence', 'NUMBER', 'intelligence'))
        self.columns.append(col('memory',       'NUMBER', 'memory'))
        self.columns.append(col('perception',   'NUMBER', 'perception'))
        self.columns.append(col('willpower',    'NUMBER', 'willpower'))