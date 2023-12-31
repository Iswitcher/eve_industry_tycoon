import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class skinLicenses(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.skins = table_skins()
        
    
    # check if all tables are present
    def check(self):
        try:
            # skins
            self.check_table(self.skins)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.skins.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_skin(self.skins.table_name, self.skins.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.skins.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update a skin        
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
        

class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_skins:
    def __init__(self):
        self.table_name = 'skin_licences'
        self.table_pk = 'skin_license_id'
        self.columns = []
        
        self.columns.append(col('skin_license_id',  'NUMBER', '#root'))
        self.columns.append(col('duration',         'NUMBER', 'duration'))
        self.columns.append(col('is_single_use',    'TEXT', 'isSingleUse'))
        self.columns.append(col('license_type_id',  'NUMBER', 'licenseTypeID'))
        self.columns.append(col('skin_id',          'NUMBER', 'skinID'))
