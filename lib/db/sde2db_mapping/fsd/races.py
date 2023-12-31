import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class races(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.races = table_races()
        self.skills = table_skills()
        
    
    # check if all tables are present
    def check(self):
        try:
            # races
            self.check_table(self.races)
            
            # skills
            self.check_table(self.skills)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.races.table_name)
            self.db.table_start_sync(self.skills.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_race(self.races.table_name, self.races.table_pk, id, row)
            self.add_skills(self.skills, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.races.table_name)
            self.db.table_finish_sync(self.skills.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update races   
    def add_race(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.races.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            
            
    def add_skills(self, table_obj, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'skills')
            if data == None:
                    return
            for item in data:
                columns = []
                values = []
                for col in table_obj.columns:
                    value = id
                    if col.name == 'skill_id':
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
    

class table_races:
    def __init__(self):
        self.table_name = 'races'
        self.table_pk = 'race_id'
        self.columns = []
        
        self.columns.append(col('race_id', 'NUMBER', '#root'))
        self.columns.append(col('name_en', 'TEXT', 'nameID/en'))
        self.columns.append(col('desc_en', 'TEXT', 'descriptionID/en'))
        self.columns.append(col('ship_type_id', 'TEXT', 'shipTypeID'))


class table_skills:
    def __init__(self):
        self.table_name = 'race_skills'
        self.table_pk = 'race_id'
        self.columns = []
        
        self.columns.append(col('race_id',  'NUMBER', '#root'))
        self.columns.append(col('skill_id', 'NUMBER', ''))
