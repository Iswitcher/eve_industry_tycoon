import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class blueprints(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.blueprints = table_blueprints()
        self.materials = table_blueprint_materials()
        self.products = table_blueprint_products()
        self.skills = table_blueprint_skills()
        self.activities = [
            'copying', 
            'invention', 
            'manufacturing', 
            'research_material', 
            'research_time',
            'reaction'
        ]
    
    # check if all tables are present
    def check(self):
        try:
            # blueprints
            self.check_table(self.blueprints)
            
            # materials
            self.check_table(self.materials)
                
            # products
            self.check_table(self.products)
                
            # skills
            self.check_table(self.skills)
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
            self.db.table_start_sync(self.blueprints.table_name)
            self.db.table_start_sync(self.materials.table_name)
            self.db.table_start_sync(self.products.table_name)
            self.db.table_start_sync(self.skills.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_blueprint(self.blueprints.table_name, self.blueprints.table_pk, id, row)
            self.add_blueprint_meta(self.materials, 'materials', id, row)
            self.add_blueprint_meta(self.products, 'products', id, row)
            self.add_blueprint_meta(self.skills, 'skills', id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.blueprints.table_name)
            self.db.table_finish_sync(self.materials.table_name)
            self.db.table_finish_sync(self.products.table_name)
            self.db.table_finish_sync(self.skills.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update a blueprint        
    def add_blueprint(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.blueprints.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # add blueprint meta info
    def add_blueprint_meta(self, table_obj, meta_type, id, row):
        try:
            for activity in self.activities:
                path = f'activities/{activity}/{meta_type}'
                data = self.yaml_value_extract(id, row, path)
                if data == None:
                    continue
                for item in data:
                    self.add_blueprint_meta_item(activity, item, table_obj, id)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_blueprint_meta_item(self, activity, item, table_obj, id):
        try:
            columns = []
            values = []
            for column in table_obj.columns:
                if column.name == 'activity':
                    value = activity
                else: 
                    value = self.yaml_value_extract(id, item, column.path)
                columns.append(column.name)
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
    

class table_blueprints:
    def __init__(self):
        self.table_name = 'blueprints'
        self.table_pk = 'blueprint_id'
        self.columns = []
        
        self.columns.append(col('blueprint_id',         'NUMBER', '#root'))
        self.columns.append(col('blueprint_type_id',    'NUMBER', 'blueprintTypeID'))
        self.columns.append(col('max_production_limit', 'NUMBER', 'maxProductionLimit'))
        self.columns.append(col('copying_time',         'NUMBER', 'activities/copying/time'))
        self.columns.append(col('manufacturing_time',   'NUMBER', 'activities/manufacturing/time'))
        self.columns.append(col('invention_time',       'NUMBER', 'activities/invention/time'))
        self.columns.append(col('material_eff_research_time','NUMBER', 'activities/research_material/time'))
        self.columns.append(col('time_eff_research_time','NUMBER', 'activities/research_time/time'))
        

class table_blueprint_materials:
    def __init__(self):
        self.table_name = 'blueprint_materials'
        self.table_pk = 'blueprint_id'
        self.columns = []
        
        self.columns.append(col('blueprint_id', 'NUMBER', '#root'))
        self.columns.append(col('activity',     'TEXT', ''))
        self.columns.append(col('type_id',      'NUMBER', 'typeID'))
        self.columns.append(col('quantity',     'NUMBER', 'quantity'))
             
        
class table_blueprint_products:
    def __init__(self):
        self.table_name = 'blueprint_products'
        self.table_pk = 'blueprint_id'
        self.columns = []
        
        self.columns.append(col('blueprint_id', 'NUMBER', '#root'))
        self.columns.append(col('activity',     'TEXT', ''))
        self.columns.append(col('type_id',      'NUMBER', 'typeID'))
        self.columns.append(col('quantity',     'NUMBER', 'quantity'))
        self.columns.append(col('probability',  'NUMBER', 'probability'))
        

class table_blueprint_skills:
    def __init__(self):
        self.table_name = 'blueprint_skills'
        self.table_pk = 'blueprint_id'
        self.columns = []
        
        self.columns.append(col('blueprint_id', 'NUMBER', '#root'))
        self.columns.append(col('activity',     'TEXT', ''))
        self.columns.append(col('type_id',      'NUMBER', 'typeID'))
        self.columns.append(col('level',        'NUMBER', 'level'))