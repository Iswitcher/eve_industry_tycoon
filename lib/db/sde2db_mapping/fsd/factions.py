import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class factions(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.factions = table_factions()
        self.members = table_member_races()
        
    
    # check if all tables are present
    def check(self):
        try:
            # factions
            self.check_table(self.factions)
            
            # members
            self.check_table(self.members)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')


    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.factions.table_name)
            self.db.table_start_sync(self.members.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    

    def run(self, id, row):
        try:
            self.add_faction(self.factions.table_name, self.factions.table_pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.factions.table_name)
            self.db.table_finish_sync(self.members.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')           
         
    
    # add or update a faction        
    def add_faction(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.factions.columns:
                value = self.yaml_value_extract(id, row, column.path)
                columns.append(column.name)
                values.append(value)
            self.db.record_add_or_replace(table, pk, id, columns, values)
            
            self.add_members(self.members.table_name, pk, id, row)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
            
    def add_members(self, table, pk, id, row):
        try:
            data = self.yaml_value_extract(id, row, 'memberRaces')
            if data == None:
                return
            for member in data:
                columns = []
                values = []
                for column in self.members.columns:
                    columns.append(column.name)
                    if column.name == 'faction_id':
                        values.append(id)
                    if column.name == 'race_id':
                        values.append(member)
                self.db.record_add_or_replace(table, pk, id, columns, values)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
        

class col:
    def __init__(self, name, type = 'TEXT', path = None):
        self.name = name
        self.type = type
        self.path = path
    

class table_factions:
    def __init__(self):
        self.table_name = 'factions'
        self.table_pk = 'faction_id'
        self.columns = []
        
        self.columns.append(col('faction_id',       'NUMBER', '#root'))
        self.columns.append(col('corporation_id',   'TEXT', 'corporationID'))
        self.columns.append(col('militia_corporation_id',   'TEXT', 'militiaCorporationID'))
        self.columns.append(col('name_en',          'TEXT', 'nameID/en'))
        self.columns.append(col('desc_en',          'TEXT', 'descriptionID/en'))
        self.columns.append(col('short_desc_en',    'TEXT', 'shortDescriptionID/en'))
        self.columns.append(col('icon_id',          'NUMBER', 'iconID'))
        self.columns.append(col('size_factor',      'NUMBER', 'sizeFactor'))
        self.columns.append(col('solar_system_id',  'NUMBER', 'solarSystemID'))
        self.columns.append(col('is_unique_name',   'TEXT', 'uniqueName'))

        
class table_member_races:
    def __init__(self):
        self.table_name = 'faction_member_races'
        self.table_pk = 'faction_id'
        self.columns = []
        
        self.columns.append(col('faction_id',             'NUMBER', '#root'))
        self.columns.append(col('race_id',                'NUMBER', ''))