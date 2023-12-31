import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class groupIDs(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.groups = table_groups()
        
    
    # check if all tables are present
    def check(self):
        try:
            # groups
            self.check_table(self.groups)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.groups.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_group(self.groups.table_name, self.groups.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.groups.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update groups   
    def add_group(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.groups.columns:
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
    

class table_groups:
    def __init__(self):
        self.table_name = 'group_ids'
        self.table_pk = 'group_id'
        self.columns = []
        
        self.columns.append(col('group_id',                 'NUMBER', '#root'))
        self.columns.append(col('anchorable',               'TEXT', 'anchorable'))
        self.columns.append(col('anchored',                 'TEXT', 'anchored'))
        self.columns.append(col('category_id',              'NUMBER', 'categoryID'))
        self.columns.append(col('fittable_non_singleton',   'TEXT', 'fittableNonSingleton'))
        self.columns.append(col('published',                'TEXT', 'published'))
        self.columns.append(col('useBasePrice',             'TEXT', 'useBasePrice'))
        self.columns.append(col('icon_id',                  'NUMBER', 'iconID'))
        self.columns.append(col('name_en',                  'NUMBER', 'name/en'))
        
        