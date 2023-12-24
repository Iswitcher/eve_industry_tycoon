import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class skins(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.skins = table_skins()
        self.types = table_types()
        
    
    # check if all tables are present
    def check(self):
        try:
            # races
            self.check_table(self.skins)
            
            # skills
            self.check_table(self.types)
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
            self.db.table_start_sync(self.skins.table_name)
            self.db.table_start_sync(self.types.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_skin(self.skins.table_name, self.skins.table_pk, id, row)
            self.add_types(self.types, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.skins.table_name)
            self.db.table_finish_sync(self.types.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update races   
    def add_skin(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.skins.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_types(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'types')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = id
                    if col.name == 'type_id':
                        value = item
                    columns.append(col.name)
                    values.append(value)
                self.db.record_add_or_replace(table_obj.table_name, table_obj.table_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
        
class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_skins:
    def __init__(self):
        self.table_name = 'skins'
        self.table_pk = 'skin_id'
        self.columns = []
        
        self.columns.append(col('skin_id',          'NUMBER', '#root'))
        self.columns.append(col('skin_material_id', 'NUMBER', 'skinMaterialID'))
        self.columns.append(col('visible_serenity', 'TEXT', 'visibleSerenity'))
        self.columns.append(col('visible_tranquility', 'TEXT', 'visibleTranquility'))
        self.columns.append(col('allow_ccp_devs',   'TEXT', 'allowCCPDevs'))
        self.columns.append(col('internal_name',    'TEXT', 'internalName'))
        self.columns.append(col('skin_desc',        'NUMBER', 'skinDescription'))


class table_types:
    def __init__(self):
        self.table_name = 'skin_types'
        self.table_pk = 'skin_id'
        self.columns = []
        
        self.columns.append(col('skin_id',  'NUMBER', '#root'))
        self.columns.append(col('type_id',  'NUMBER', ''))
