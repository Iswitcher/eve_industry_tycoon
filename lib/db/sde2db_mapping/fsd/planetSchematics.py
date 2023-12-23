import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class planetSchematics(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.planets = table_planets()
        self.types = table_types()
        self.pins = table_pins()
        
    
    # check if all tables are present
    def check(self):
        try:
            # planets
            self.check_table(self.planets)
            
            # types
            self.check_table(self.types)
            
            # pins
            self.check_table(self.pins)
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
            self.db.table_start_sync(self.planets.table_name)
            self.db.table_start_sync(self.types.table_name)
            self.db.table_start_sync(self.pins.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_planets(self.planets.table_name, self.planets.table_pk, id, row)
            self.add_types(self.types, id, row)
            self.add_pins(self.pins, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.planets.table_name)
            self.db.table_finish_sync(self.types.table_name)
            self.db.table_finish_sync(self.pins.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update npc_corps   
    def add_planets(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.planets.columns:
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
                    value = self.yaml_value_extract(id, data[item], col.path)
                    if col.name == 'planet_schematics_type_id':
                        value = item
                    columns.append(col.name)
                    values.append(value)    
                self.db.record_add_or_replace(table_obj.table_name, table_obj.table_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_pins(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'pins')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = id
                    if col.name == 'pin_id':
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
    

class table_planets:
    def __init__(self):
        self.table_name = 'planet_schematics'
        self.table_pk = 'planet_schematics_id'
        self.columns = []
        
        self.columns.append(col('planet_schematics_id', 'NUMBER', '#root'))
        self.columns.append(col('cycle_time',           'NUMBER', 'cycleTime'))
        self.columns.append(col('name_en',              'TEXT', 'nameID/en'))


class table_types:
    def __init__(self):
        self.table_name = 'planet_schematics_types'
        self.table_pk = 'planet_schematics_id'
        self.columns = []
        
        self.columns.append(col('planet_schematics_id',     'NUMBER', '#root'))
        self.columns.append(col('planet_schematics_type_id','NUMBER', ''))
        self.columns.append(col('is_input',                 'TEXT', 'isInput'))
        self.columns.append(col('quantity',                 'NUMBER', 'quantity'))
        


class table_pins:
    def __init__(self):
        self.table_name = 'planet_schematics_pins'
        self.table_pk = 'planet_schematics_id'
        self.columns = []
        
        self.columns.append(col('planet_schematics_id',      'NUMBER', '#root'))
        self.columns.append(col('pin_id',      'NUMBER', ''))
