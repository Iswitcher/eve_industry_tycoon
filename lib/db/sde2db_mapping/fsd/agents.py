import traceback

from lib.db.sde2db_mapping.sde_mapper import mapper
from lib.db.db_utils import db_utils
from lib.logger import logger

class agents(mapper):
    
    def __init__(self, db: db_utils, log:logger):
        self.db = db
        self.log = log
        self.agents = table_agents()
        

    # check if all tables are present
    def check(self):
        try:
            # agents
            if not self.db.table_check(self.agents.table_name):
                self.db.table_create(self.agents.table_name)
            agent_cols = [] 
            agent_types = []
            for column in self.agents.columns:
                agent_cols.append(column.name)
                agent_types.append(column.type)
            self.db.table_column_check(self.agents.table_name, agent_cols, agent_types)
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
            

    # add new row
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
    

class table_agents:
    def __init__(self):
        self.table_name = 'agents'
        self.table_pk = 'agent_id'
        self.columns = []
        
        self.columns.append(col('agent_id',       'NUMBER', '#root'))
        self.columns.append(col('agent_type_id',  'NUMBER', 'agentTypeID'))
        self.columns.append(col('corporation_id', 'NUMBER', 'corporationID'))
        self.columns.append(col('division_id',    'NUMBER', 'divisionID'))
        self.columns.append(col('is_locator',     'NUMBER', 'isLocator'))
        self.columns.append(col('level',          'NUMBER', 'level'))
        self.columns.append(col('location_id',    'NUMBER', 'locationID'))
        

        