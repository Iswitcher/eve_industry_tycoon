import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class npcCorporationDivisions(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.corp_divisions = table_corp_divisions()
        
    
    # check if all tables are present
    def check(self):
        try:
            # corp_divisions
            self.check_table(self.corp_divisions)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.corp_divisions.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_corp_division(self.corp_divisions.table_name, self.corp_divisions.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.corp_divisions.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update corp_divisions   
    def add_corp_division(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.corp_divisions.columns:
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
    

class table_corp_divisions:
    def __init__(self):
        self.table_name = 'npc_corp_divisions'
        self.table_pk = 'npc_corp_division_id'
        self.columns = []
        
        self.columns.append(col('npc_corp_division_id',     'NUMBER', '#root'))
        self.columns.append(col('description',          'TEXT', 'description'))
        self.columns.append(col('internalName',         'TEXT', 'internalName'))
        self.columns.append(col('leader_type_name_en',  'TEXT', 'leaderTypeNameID/en'))
        self.columns.append(col('name_en',              'TEXT', 'nameID/en'))
        self.columns.append(col('desc_en',              'TEXT', 'descriptionID/en'))
        