import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class agentsInSpace(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log        
        self.agents = table_agentsInSpace()


    # check if all tables are present
    def check(self):
        try:
            # agents
            self.check_table(self.agents)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')

    
    # start the import
    def start(self):
        try:
            self.db.table_start_sync(self.agents.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
            

    def run(self, id, row):
        try:
            self.add_agent(self.agents.table_name, self.agents.table_pk, id, row) 
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')
    
    
    # complete the import
    def finish(self):
        try:
            self.db.table_finish_sync(self.agents.table_name)
        except Exception as e:
            method_name = traceback.extract_stack(None, 2)[0][2]
            self.log.critical(f'ERROR in {method_name}: {e}')  
         
    
    # add or update an agent        
    def add_agent(self, table, pk, id, row):
        try:
            columns = []
            values = []
            
            for column in self.agents.columns:
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
    

class table_agentsInSpace:
    def __init__(self):
        self.table_name = 'agents_in_space'
        self.table_pk = 'agent_id'
        self.columns = []
        
        self.columns.append(col('agent_id',         'NUMBER', '#root'))
        self.columns.append(col('dungeon_id',       'NUMBER', 'dungeonID'))
        self.columns.append(col('solar_system_id',  'NUMBER', 'solarSystemID'))
        self.columns.append(col('spawn_point_id',   'NUMBER', 'spawnPointID'))
        self.columns.append(col('type_id',          'NUMBER', 'typeID'))
        
