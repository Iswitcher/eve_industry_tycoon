import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class blueprints(mapper):
    
    def __init__(self, db_path, yaml, log):
        self.db_path = db_path
        self.yaml = yaml
        self.log = log
        self.db = db_utils(self.log, self.db_path, None)
        
        self.table_blueprints = 'blueprints'
        self.table_blueprints_pk = 'blueprint_id'
        self.table_blueprints_columns = []


    def run(self):
        try:
            self.db.db_check()
            self.db.db_connect()
            
            self.check_tables_and_columns()
            self.sync()
            
            self.db.db_commit()
            self.db.db_disconnect()
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
    
    #go row by row and fill each table
    def sync(self):
        try:
            self.db.table_start_sync(self.table_blueprints)
            for row in self.yaml:
                # add row to blueprints table
                self.add_blueprint(self.table_blueprints, self.table_blueprints_pk, row, self.yaml[row]) 
            self.db.table_finish_sync(self.table_blueprints)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    # check all class-cpecific tables and columns
    def check_tables_and_columns(self):
        try:
            # blueprints
            if not self.db.table_check(self.table_blueprints):
                self.db.table_create(self.table_blueprints)
            columns, types = self.get_blueprint_columns()
            self.db.table_column_check(self.table_blueprints, columns, types)  
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    # get yaml value by path or fill None if not found
    def yaml_value_extract(self, yaml_row, path):
        path_array = path.split('/')
        result = yaml_row
        try:
            for node in path_array:
                result = result.get(node)
            return result
        except (KeyError, TypeError):
            return None
    

    # get the list of columns in table: blueprints
    def get_blueprint_columns(self, columns = [], types = []):
        columns.append('blueprint_id')
        types.append('NUMBER')
        
        columns.append('blueprint_type_id')
        types.append('NUMBER')
        
        columns.append('max_production_limit')
        types.append('NUMBER')
        
        columns.append('copying_time')
        types.append('NUMBER')
        
        columns.append('manufacturing_time')
        types.append('NUMBER')
        
        columns.append('invention_time')
        types.append('NUMBER')
        
        columns.append('material_eff_research_time')
        types.append('NUMBER')
        
        columns.append('time_eff_research_time')
        types.append('NUMBER')
        
        return columns, types    
         
    
    # add or update a blueprint        
    def add_blueprint(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            columns.append('blueprint_id')
            values.append(id)
            
            columns.append('blueprint_type_id')
            values.append(self.yaml_value_extract(row, 'blueprintTypeID'))
            
            columns.append('max_production_limit')
            values.append(self.yaml_value_extract(row, 'maxProductionLimit'))
            
            columns.append('copying_time')
            values.append(self.yaml_value_extract(row, 'activities/copying/time'))
            
            columns.append('manufacturing_time')
            values.append(self.yaml_value_extract(row, 'activities/manufacturing/time'))
            
            columns.append('invention_time')
            blah = self.yaml_value_extract(row, 'activities/invention/time')
            values.append(self.yaml_value_extract(row, 'activities/invention/time'))
            
            columns.append('material_eff_research_time')
            values.append(self.yaml_value_extract(row, 'activities/research_material/time'))
            
            columns.append('time_eff_research_time')
            values.append(self.yaml_value_extract(row, 'activities/research_time/time'))

            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    

