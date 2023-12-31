import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class certificates(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.certificates = table_certificates()
        self.recommended = table_recommended()
        self.skill_types = table_skill_types()
        
    
    # check if all tables are present
    def check(self):
        try:
            # certificates
            self.check_table(self.certificates)
            
            # recommended
            self.check_table(self.recommended)
                
            # skills
            self.check_table(self.skill_types)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.certificates.table_name)
            self.db.table_start_sync(self.recommended.table_name)
            self.db.table_start_sync(self.skill_types.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_certificate(self.certificates.table_name, self.certificates.table_pk, id, row)
            self.add_recommended(self.recommended, id, row)
            self.add_skill_types(self.skill_types, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.certificates.table_name)
            self.db.table_finish_sync(self.recommended.table_name)
            self.db.table_finish_sync(self.skill_types.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update a certificate        
    def add_certificate(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.certificates.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # add or update a certificate recommended types
    def add_recommended(self, table_obj, id, row):
        try:
            path = f'recommendedFor'
            data = self.yaml_value_extract(id, row, path)
            if data == None:
                return
            for type in data:
                columns = []
                for col in table_obj.columns:
                    columns.append(col.name)
                values = []
                values.append(id)
                values.append(type)
                self.db.record_add_or_replace(table_obj.table_name, table_obj.table_pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # add or update skill types data
    def add_skill_types(self, table_obj, id, row):
        try:
            path = f'skillTypes'
            data = self.yaml_value_extract(id, row, path)
            if data == None:
                return
            for item in data:
                self.add_skill_type(self.skill_types, id, item, data[item])
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    # add skill type
    def add_skill_type(self, table_obj, id, item, data):
        try:
            columns = []
            values = []
            for col in table_obj.columns:
                value = self.yaml_value_extract(id, data, col.path)
                if col.name == 'skill_type_id':
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
    

class table_certificates:
    def __init__(self):
        self.table_name = 'certificates'
        self.table_pk = 'certificate_id'
        self.columns = []
        
        self.columns.append(col('certificate_id',   'NUMBER', '#root'))
        self.columns.append(col('description',      'TEXT', 'description'))
        self.columns.append(col('group_id',         'NUMBER', 'groupID'))
        self.columns.append(col('name',             'TEXT', 'name'))
     

class table_recommended:
    def __init__(self):
        self.table_name = 'certificate_recommended_for_type'
        self.table_pk = 'certificate_id'
        self.columns = []
        
        self.columns.append(col('certificate_id', 'NUMBER', '#root'))
        self.columns.append(col('recommended_for_type_id',     'NUMBER', ''))
        

class table_skill_types:
    def __init__(self):
        self.table_name = 'certificate_skill_types'
        self.table_pk = 'certificate_id'
        self.columns = []
        
        self.columns.append(col('certificate_id',   'NUMBER', '#root'))
        self.columns.append(col('skill_type_id',    'NUMBER', ''))
        self.columns.append(col('basic',            'TEXT', 'basic'))
        self.columns.append(col('standard',         'TEXT', 'standard'))
        self.columns.append(col('improved',         'TEXT', 'improved'))
        self.columns.append(col('advanced',         'TEXT', 'advanced'))
        self.columns.append(col('elite',            'TEXT', 'elite'))