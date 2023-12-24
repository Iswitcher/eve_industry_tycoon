import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class typeMaterials(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.materials = table_materials()
        
    
    # check if all tables are present
    def check(self):
        try:
            # materials
            self.check_table(self.materials)
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
            self.db.table_start_sync(self.materials.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_dogma(self.materials, id, row, 'materials')
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.materials.table_name)
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
    

class table_materials:
    def __init__(self):
        self.table_name = 'type_materials'
        self.table_pk = 'type_id'
        self.columns = []
        
        self.columns.append(col('type_id',          'NUMBER', '#root'))
        self.columns.append(col('material_type_id', 'NUMBER', 'materialTypeID'))
        self.columns.append(col('quantity',         'NUMBER', 'quantity'))
        