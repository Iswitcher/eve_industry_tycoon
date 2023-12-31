import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class stationOperations(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.operations = table_operations()
        self.services = table_services()
        self.types = table_types()
        
    
    # check if all tables are present
    def check(self):
        try:
            # operations
            self.check_table(self.operations)
            
            # services
            self.check_table(self.services)
            
            # types
            self.check_table(self.types)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.operations.table_name)
            self.db.table_start_sync(self.services.table_name)
            self.db.table_start_sync(self.types.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_operation(self.operations.table_name, self.operations.table_pk, id, row)
            self.add_service(self.services, id, row)
            self.add_type(self.types, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.operations.table_name)
            self.db.table_finish_sync(self.services.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update operations   
    def add_operation(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.operations.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_service(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'services')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = id
                    if col.name == 'service_id':
                        value = item
                    columns.append(col.name)
                    values.append(value)
                self.db.record_add_or_replace(table_obj.table_name, table_obj.table_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_type(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'stationTypes')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = self.yaml_value_extract(id, row, col.path)
                    if col.name == 'type_id':
                        value = item
                    elif col.name == 'type_value':
                        value = data[item]
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
    

class table_operations:
    def __init__(self):
        self.table_name = 'station_operations'
        self.table_pk = 'station_operation_id'
        self.columns = []
        
        self.columns.append(col('station_operation_id', 'NUMBER', '#root'))
        self.columns.append(col('activity_id',          'NUMBER', 'activityID'))
        self.columns.append(col('border',               'NUMBER', 'border'))
        self.columns.append(col('corridor',             'NUMBER', 'corridor'))
        self.columns.append(col('desc_en',              'TEXT', 'descriptionID/en'))
        self.columns.append(col('operation_name_en',    'TEXT', 'operationNameID/en'))
        self.columns.append(col('ratio',                'NUMBER', 'ratio'))
        self.columns.append(col('fringe',               'NUMBER', 'fringe'))
        self.columns.append(col('hub',                  'NUMBER', 'hub'))
        self.columns.append(col('manufacturing_factor', 'NUMBER', 'manufacturingFactor'))
        self.columns.append(col('research_factor',      'NUMBER', 'researchFactor'))


class table_services:
    def __init__(self):
        self.table_name = 'station_services'
        self.table_pk = 'station_operation_id'
        self.columns = []
        
        self.columns.append(col('station_operation_id',  'NUMBER', '#root'))
        self.columns.append(col('service_id', 'NUMBER', ''))
        
        
class table_types:
    def __init__(self):
        self.table_name = 'station_types'
        self.table_pk = 'station_operation_id'
        self.columns = []
        
        self.columns.append(col('station_operation_id',  'NUMBER', '#root'))
        self.columns.append(col('type_id', 'NUMBER', ''))
        self.columns.append(col('type_value', 'NUMBER', ''))
