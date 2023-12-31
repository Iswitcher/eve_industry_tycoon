import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class graphicIDs(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.graphics = table_graphics()
        
    
    # check if all tables are present
    def check(self):
        try:
            # graphics
            self.check_table(self.graphics)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.graphics.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_graphics(self.graphics.table_name, self.graphics.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.graphics.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update graphics        
    def add_graphics(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.graphics.columns:
                value = self.yaml_value_extract(id, row, column.path)
                if type(value) == list:
                    value = str(value)
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
    

class table_graphics:
    def __init__(self):
        self.table_name = 'graphic_ids'
        self.table_pk = 'graphic_id'
        self.columns = []
        
        self.columns.append(col('graphic_id',       'NUMBER', '#root'))
        self.columns.append(col('description',      'TEXT', 'description'))
        self.columns.append(col('sof_faction_name', 'TEXT', 'sofFactionName'))
        self.columns.append(col('sof_hull_name',    'TEXT', 'sofHullName'))
        self.columns.append(col('sof_race_name',    'TEXT', 'sofRaceName'))
        self.columns.append(col('graphic_file',     'TEXT', 'graphicFile'))
        self.columns.append(col('sof_layout',       'TEXT', 'sofLayout'))
        self.columns.append(col('icon_info_folder', 'TEXT', 'iconInfo/folder'))