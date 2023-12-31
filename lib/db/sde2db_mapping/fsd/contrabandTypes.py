import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class contrabandTypes(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.contraband = table_contraband()
        
    
    # check if all tables are present
    def check(self):
        try:
            # contrabandTypes
            self.check_table(self.contraband)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.contraband.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_contraband(self.contraband.table_name, self.contraband.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.contraband.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update a contraband       
    def add_contraband(self, table, pk, id, row):
        try:
            for faction in row['factions']:            
                columns = []
                values = []
                data = row['factions'][faction]
                for column in self.contraband.columns:
                    value = self.yaml_value_extract(id, data, column.path)
                    if column.name == 'faction_id':
                        value = faction
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
    

class table_contraband:
    def __init__(self):
        self.table_name = 'contraband_types'
        self.table_pk = 'contraband_type_id'
        self.columns = []
        
        self.columns.append(col('contraband_type_id', 'NUMBER', '#root'))
        self.columns.append(col('faction_id',         'NUMBER', ''))
        self.columns.append(col('attack_min_sec',     'NUMBER', 'attackMinSec'))
        self.columns.append(col('confiscate_min_sec', 'NUMBER', 'confiscateMinSec'))
        self.columns.append(col('fine_by_value',      'NUMBER', 'fineByValue'))
        self.columns.append(col('standing_loss',      'NUMBER', 'standingLoss'))